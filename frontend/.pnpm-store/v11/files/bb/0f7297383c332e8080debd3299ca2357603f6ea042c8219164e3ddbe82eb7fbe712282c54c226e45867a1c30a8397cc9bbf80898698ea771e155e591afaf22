Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });

const core = require('@sentry/core');
const debugBuild = require('../common/debug-build.js');
const utils = require('./utils.js');

const FETCH_PROXY_SCRIPT = `
    const f = window.fetch;
    if(f){
      window._sentryFetchProxy = function(...a){return f(...a)}
      window.fetch = function(...a){return window._sentryFetchProxy(...a)}
    }
`;
/**
 * Adds Sentry tracing <meta> tags to the returned html page.
 * Adds Sentry fetch proxy script to the returned html page if enabled in options.
 *
 * Exported only for testing
 */
function addSentryCodeToPage(options

) {
  return ({ html }) => {
    const metaTags = core.getTraceMetaTags();
    const headWithMetaTags = metaTags ? `<head>\n${metaTags}` : '<head>';

    const headWithFetchScript = options.injectFetchProxyScript ? `\n<script>${FETCH_PROXY_SCRIPT}</script>` : '';

    const modifiedHead = `${headWithMetaTags}${headWithFetchScript}`;

    return html.replace('<head>', modifiedHead);
  };
}

/**
 * We only need to inject the fetch proxy script for SvelteKit versions < 2.16.0.
 * Exported only for testing.
 */
function isFetchProxyRequired(version) {
  try {
    const [major, minor] = version.trim().replace(/-.*/, '').split('.').map(Number);
    if (major != null && minor != null && (major > 2 || (major === 2 && minor >= 16))) {
      return false;
    }
  } catch {
    // ignore
  }
  return true;
}

async function instrumentHandle(
  {
    event,
    resolve,
  }

,
  options,
) {
  const routeId = event.route?.id;

  if (!routeId && !options.handleUnknownRoutes) {
    return resolve(event);
  }

  // caching the result of the version check in `options.injectFetchProxyScript`
  // to avoid doing the dynamic import on every request
  if (options.injectFetchProxyScript == null) {
    try {
      // @ts-expect-error - the dynamic import is fine here
      const { VERSION } = await import('@sveltejs/kit');
      options.injectFetchProxyScript = isFetchProxyRequired(VERSION);
    } catch {
      options.injectFetchProxyScript = true;
    }
  }

  const routeName = `${event.request.method} ${routeId || event.url.pathname}`;

  if (core.getIsolationScope() !== core.getDefaultIsolationScope()) {
    core.getIsolationScope().setTransactionName(routeName);
  } else {
    debugBuild.DEBUG_BUILD && core.debug.warn('Isolation scope is default isolation scope - skipping setting transactionName');
  }

  // We only start a span if SvelteKit's native tracing is not enabled. Two reasons:
  // - Used Kit version doesn't yet support tracing
  // - Users didn't enable tracing
  const kitTracingEnabled = event.tracing?.enabled;

  try {
    const resolveWithSentry = async (sentrySpan) => {
      core.getCurrentScope().setSDKProcessingMetadata({
        // We specifically avoid cloning the request here to avoid double read errors.
        // We only read request headers so we're not consuming the body anyway.
        // Note to future readers: This sounds counter-intuitive but please read
        // https://github.com/getsentry/sentry-javascript/issues/14583
        normalizedRequest: core.winterCGRequestToRequestData(event.request),
      });
      const kitRootSpan = event.tracing?.enabled ? event.tracing?.root : undefined;

      if (kitRootSpan) {
        // Update the root span emitted from SvelteKit to resemble a `http.server` span
        // We're doing this here instead of an event processor to ensure we update the
        // span name as early as possible (for dynamic sampling, et al.)
        // Other spans are enhanced in the `processKitSpans` integration.
        const spanJson = core.spanToJSON(kitRootSpan);
        const kitRootSpanAttributes = spanJson.data;
        const originalName = spanJson.description;

        const routeName = kitRootSpanAttributes['http.route'];
        if (routeName && typeof routeName === 'string') {
          core.updateSpanName(kitRootSpan, `${event.request.method ?? 'GET'} ${routeName}`);
        }

        kitRootSpan.setAttributes({
          [core.SEMANTIC_ATTRIBUTE_SENTRY_OP]: 'http.server',
          [core.SEMANTIC_ATTRIBUTE_SENTRY_ORIGIN]: 'auto.http.sveltekit',
          [core.SEMANTIC_ATTRIBUTE_SENTRY_SOURCE]: routeName ? 'route' : 'url',
          'sveltekit.tracing.original_name': originalName,
          ...core.httpHeadersToSpanAttributes(
            core.winterCGHeadersToDict(event.request.headers),
            core.getClient()?.getOptions().sendDefaultPii ?? false,
          ),
        });
      }

      const res = await resolve(event, {
        transformPageChunk: addSentryCodeToPage({
          injectFetchProxyScript: options.injectFetchProxyScript ?? true,
        }),
      });

      if (sentrySpan) {
        core.setHttpStatus(sentrySpan, res.status);
      }

      return res;
    };

    const resolveResult = kitTracingEnabled
      ? await resolveWithSentry()
      : await core.startSpan(
          {
            op: 'http.server',
            attributes: {
              [core.SEMANTIC_ATTRIBUTE_SENTRY_ORIGIN]: 'auto.http.sveltekit',
              [core.SEMANTIC_ATTRIBUTE_SENTRY_SOURCE]: routeId ? 'route' : 'url',
              'http.method': event.request.method,
              ...core.httpHeadersToSpanAttributes(
                core.winterCGHeadersToDict(event.request.headers),
                core.getClient()?.getOptions().sendDefaultPii ?? false,
              ),
            },
            name: routeName,
          },
          resolveWithSentry,
        );

    return resolveResult;
  } catch (e) {
    utils.sendErrorToSentry(e, 'handle');
    throw e;
  } finally {
    await core.flushIfServerless();
  }
}

/**
 * A SvelteKit handle function that wraps the request for Sentry error and
 * performance monitoring.
 *
 * Usage:
 * ```
 * // src/hooks.server.ts
 * import { sentryHandle } from '@sentry/sveltekit';
 *
 * export const handle = sentryHandle();
 *
 * // Optionally use the `sequence` function to add additional handlers.
 * // export const handle = sequence(sentryHandle(), yourCustomHandler);
 * ```
 */
function sentryHandle(handlerOptions) {
  const { handleUnknownRoutes, ...rest } = handlerOptions ?? {};
  const options = {
    handleUnknownRoutes: handleUnknownRoutes ?? false,
    ...rest,
  };

  const sentryRequestHandler = input => {
    const backwardsForwardsCompatibleEvent = input.event ;

    // Escape hatch to suppress request isolation and trace continuation (see initCloudflareSentryHandle)
    const skipIsolation =
      '_sentrySkipRequestIsolation' in backwardsForwardsCompatibleEvent.locals &&
      backwardsForwardsCompatibleEvent.locals._sentrySkipRequestIsolation;

    // In case of a same-origin `fetch` call within a server`load` function,
    // SvelteKit will actually just re-enter the `handle` function and set `isSubRequest`
    // to `true` so that no additional network call is made.
    // We want the `http.server` span of that nested call to be a child span of the
    // currently active span instead of a new root span to correctly reflect this
    // behavior.
    if (skipIsolation || input.event.isSubRequest) {
      return instrumentHandle(input, {
        ...options,
      });
    }

    return core.withIsolationScope(isolationScope => {
      // We only call continueTrace in the initial top level request to avoid
      // creating a new root span for the sub request.
      isolationScope.setSDKProcessingMetadata({
        // We specifically avoid cloning the request here to avoid double read errors.
        // We only read request headers so we're not consuming the body anyway.
        // Note to future readers: This sounds counter-intuitive but please read
        // https://github.com/getsentry/sentry-javascript/issues/14583
        normalizedRequest: core.winterCGRequestToRequestData(input.event.request),
      });

      if (backwardsForwardsCompatibleEvent.tracing?.enabled) {
        // if sveltekit tracing is enabled (since 2.31.0), trace continuation is handled by
        // kit before our hook is executed. No noeed to call `continueTrace` from our end
        return instrumentHandle(input, options);
      }

      return core.continueTrace(utils.getTracePropagationData(input.event), () => instrumentHandle(input, options));
    });
  };

  return sentryRequestHandler;
}

exports.FETCH_PROXY_SCRIPT = FETCH_PROXY_SCRIPT;
exports.addSentryCodeToPage = addSentryCodeToPage;
exports.isFetchProxyRequired = isFetchProxyRequired;
exports.sentryHandle = sentryHandle;
//# sourceMappingURL=handle.js.map
