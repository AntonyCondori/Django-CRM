Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });

const svelte = require('@sentry/svelte');
const sdk = require('./client/sdk.js');
const handleError = require('./client/handleError.js');
const load = require('./client/load.js');
const browserTracingIntegration = require('./client/browserTracingIntegration.js');



exports.init = sdk.init;
exports.handleErrorWithSentry = handleError.handleErrorWithSentry;
exports.wrapLoadWithSentry = load.wrapLoadWithSentry;
exports.browserTracingIntegration = browserTracingIntegration.browserTracingIntegration;
Object.prototype.hasOwnProperty.call(svelte, '__proto__') &&
	!Object.prototype.hasOwnProperty.call(exports, '__proto__') &&
	Object.defineProperty(exports, '__proto__', {
		enumerable: true,
		value: svelte['__proto__']
	});

Object.keys(svelte).forEach(k => {
	if (k !== 'default' && !Object.prototype.hasOwnProperty.call(exports, k)) exports[k] = svelte[k];
});
//# sourceMappingURL=index.client.js.map
