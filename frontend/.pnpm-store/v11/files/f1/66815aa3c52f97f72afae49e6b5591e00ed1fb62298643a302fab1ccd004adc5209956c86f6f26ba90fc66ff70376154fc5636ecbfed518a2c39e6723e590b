Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });

const core = require('@sentry/core');
const node = require('@sentry/node');
const rewriteFramesIntegration = require('../server-common/integrations/rewriteFramesIntegration.js');
const svelteKitSpans = require('../server-common/integrations/svelteKitSpans.js');
const http = require('./integrations/http.js');

/**
 * Initialize the Server-side Sentry SDK
 * @param options
 */
function init(options) {
  const defaultIntegrations = [
    ...node.getDefaultIntegrations(options).filter(integration => integration.name !== 'Http'),
    rewriteFramesIntegration.rewriteFramesIntegration(),
    http.httpIntegration(),
    svelteKitSpans.svelteKitSpansIntegration(),
  ];

  const opts = {
    defaultIntegrations,
    ...options,
  };

  core.applySdkMetadata(opts, 'sveltekit', ['sveltekit', 'node']);

  return node.init(opts);
}

exports.init = init;
//# sourceMappingURL=sdk.js.map
