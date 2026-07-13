Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });

const core = require('@sentry/core');
const svelte = require('@sentry/svelte');
const browserTracingIntegration = require('./browserTracingIntegration.js');

/**
 * Initialize the client side of the Sentry SvelteKit SDK.
 *
 * @param options Configuration options for the SDK.
 */
function init(options) {
  const opts = {
    defaultIntegrations: getDefaultIntegrations(options),
    ...options,
  };

  core.applySdkMetadata(opts, 'sveltekit', ['sveltekit', 'svelte']);

  // 1. Switch window.fetch to our fetch proxy we injected earlier
  const actualFetch = switchToFetchProxy();

  // 2. Initialize the SDK which will instrument our proxy
  const client = svelte.init(opts);

  // 3. Restore the original fetch now that our proxy is instrumented
  if (actualFetch) {
    restoreFetch(actualFetch);
  }

  return client;
}

function getDefaultIntegrations(options) {
  // This evaluates to true unless __SENTRY_TRACING__ is text-replaced with "false",
  // in which case everything inside will get tree-shaken away
  if (typeof __SENTRY_TRACING__ === 'undefined' || __SENTRY_TRACING__) {
    return [...svelte.getDefaultIntegrations(options), browserTracingIntegration.browserTracingIntegration()];
  }

  return svelte.getDefaultIntegrations(options);
}

/**
 * During server-side page load, we injected a <script> that wraps `window.fetch` so that
 * before a `fetch` call is forwarded to the original `window.fetch`, a function we control
 * is also invoked. This function is put onto the global object (`window._sentryFetchProxy`)
 * so that we can access it here.
 *
 * In this function we briefly set our fetch proxy as `window.fetch` so that the SDK can
 * instrument it.
 *
 * After initializing the SDK, `restoreFetch` must be called to put back whatever was on `window.fetch` before.
 *
 * @see ../server/handle.ts (https://github.com/getsentry/sentry-javascript/blob/8d92180c900c2ac98fd127d53703a415c1f191dd/packages/sveltekit/src/server/handle.ts#L60-L81)
 *
 * @returns the function that was previously on `window.fetch`.
 */
function switchToFetchProxy() {
  const globalWithSentryFetchProxy = svelte.WINDOW;

  // eslint-disable-next-line @typescript-eslint/unbound-method
  const actualFetch = globalWithSentryFetchProxy.fetch;

  if (globalWithSentryFetchProxy._sentryFetchProxy && actualFetch) {
    globalWithSentryFetchProxy.fetch = globalWithSentryFetchProxy._sentryFetchProxy;
    return actualFetch;
  }
  return undefined;
}

/**
 * Restores the function @param actualFetch to `window.fetch`
 * and puts our fetch proxy back onto `window._sentryFetchProxy`.
 */
function restoreFetch(actualFetch) {
  const globalWithSentryFetchProxy = svelte.WINDOW;

  // eslint-disable-next-line @typescript-eslint/unbound-method
  globalWithSentryFetchProxy._sentryFetchProxy = globalWithSentryFetchProxy.fetch;
  globalWithSentryFetchProxy.fetch = actualFetch;
}

exports.init = init;
//# sourceMappingURL=sdk.js.map
