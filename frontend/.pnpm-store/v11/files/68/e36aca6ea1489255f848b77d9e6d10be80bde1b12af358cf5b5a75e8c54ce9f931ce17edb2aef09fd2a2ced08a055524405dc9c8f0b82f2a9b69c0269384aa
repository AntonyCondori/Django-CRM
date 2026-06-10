Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });

const cloudflare = require('@sentry/cloudflare');
const core = require('@sentry/core');
const rewriteFramesIntegration = require('../server-common/integrations/rewriteFramesIntegration.js');
const svelteKitSpans = require('../server-common/integrations/svelteKitSpans.js');

/**
 *  Initializes Sentry SvelteKit Cloudflare SDK
 *  This should be before the sentryHandle() call.
 *
 *  In the Node export, this is a stub that does nothing.
 */
function initCloudflareSentryHandle(options) {
  const opts = {
    defaultIntegrations: [
      ...cloudflare.getDefaultIntegrations(options),
      rewriteFramesIntegration.rewriteFramesIntegration(),
      svelteKitSpans.svelteKitSpansIntegration(),
    ],
    ...options,
  };

  cloudflare.setAsyncLocalStorageAsyncContextStrategy();

  const handleInitSentry = ({ event, resolve }) => {
    // if event.platform exists (should be there in a cloudflare worker), then do the cloudflare sentry init
    if (event.platform) {
      // This is an optional local that the `sentryHandle` handler checks for to avoid double isolation
      // In Cloudflare the `wrapRequestHandler` function already takes care of
      // - request isolation
      // - trace continuation
      // -setting the request onto the scope
      core.addNonEnumerableProperty(event.locals, '_sentrySkipRequestIsolation', true);
      return cloudflare.wrapRequestHandler(
        {
          options: opts,
          request: event.request,
          // @ts-expect-error This will exist in Cloudflare
          context: event.platform.context,
          // We don't want to capture errors here, as we want to capture them in the `sentryHandle` handler
          // where we can distinguish between redirects and actual errors.
          captureErrors: false,
        },
        () => resolve(event),
      );
    }
    return resolve(event);
  };

  return handleInitSentry;
}

exports.initCloudflareSentryHandle = initCloudflareSentryHandle;
//# sourceMappingURL=cloudflare.js.map
