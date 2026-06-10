import { applySdkMetadata } from '@sentry/core';
import { getDefaultIntegrations, init as init$1 } from '@sentry/node';
import { rewriteFramesIntegration } from '../server-common/integrations/rewriteFramesIntegration.js';
import { svelteKitSpansIntegration } from '../server-common/integrations/svelteKitSpans.js';
import { httpIntegration } from './integrations/http.js';

/**
 * Initialize the Server-side Sentry SDK
 * @param options
 */
function init(options) {
  const defaultIntegrations = [
    ...getDefaultIntegrations(options).filter(integration => integration.name !== 'Http'),
    rewriteFramesIntegration(),
    httpIntegration(),
    svelteKitSpansIntegration(),
  ];

  const opts = {
    defaultIntegrations,
    ...options,
  };

  applySdkMetadata(opts, 'sveltekit', ['sveltekit', 'node']);

  return init$1(opts);
}

export { init };
//# sourceMappingURL=sdk.js.map
