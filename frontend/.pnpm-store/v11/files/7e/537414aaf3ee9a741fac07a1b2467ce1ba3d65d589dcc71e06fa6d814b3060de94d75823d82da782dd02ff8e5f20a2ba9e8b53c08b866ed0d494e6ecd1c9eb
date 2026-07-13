import { init } from './sdk.js';

/**
 * Actual implementation in ../worker/handle.ts
 *
 * This handler initializes the Sentry Node(!) SDK with the passed options. This is necessary to get
 * the SDK configured for cloudflare working in dev mode.
 *
 * @return version of initCLoudflareSentryHandle that is called via node/server entry point
 */
function initCloudflareSentryHandle(options) {
  let sentryInitialized = false;

  return ({ event, resolve }) => {
    if (!sentryInitialized) {
      sentryInitialized = true;
      init(options);
    }

    return resolve(event);
  };
}

export { initCloudflareSentryHandle };
//# sourceMappingURL=handle.js.map
