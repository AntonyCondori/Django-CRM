Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });

const browser = require('@sentry/browser');
const core = require('@sentry/core');

/**
 * Inits the Svelte SDK
 */
function init(options) {
  const opts = {
    ...options,
  };

  core.applySdkMetadata(opts, 'svelte');

  return browser.init(opts);
}

exports.init = init;
//# sourceMappingURL=sdk.js.map
