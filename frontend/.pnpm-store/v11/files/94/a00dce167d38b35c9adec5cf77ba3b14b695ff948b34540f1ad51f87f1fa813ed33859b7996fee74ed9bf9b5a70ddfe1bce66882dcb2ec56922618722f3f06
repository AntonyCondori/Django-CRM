Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });

const core = require('@sentry/core');
const debugBuild = require('../debug-build.js');

const INTEGRATION_NAME = 'Hono';

/** Only exported for internal use */
function getHonoIntegration() {
  return core.getClient()?.getIntegrationByName(INTEGRATION_NAME);
}

function isHonoError(err) {
  if (err instanceof Error) {
    return true;
  }
  return typeof err === 'object' && err !== null && 'status' in (err );
}

// Vendored from https://github.com/honojs/hono/blob/d3abeb1f801aaa1b334285c73da5f5f022dbcadb/src/helper/route/index.ts#L58-L59
const routePath = (c) => c.req?.path ?? '';

const _honoIntegration = ((options = {}) => {
  return {
    name: INTEGRATION_NAME,
    // Hono error handler: https://github.com/honojs/hono/blob/d3abeb1f801aaa1b334285c73da5f5f022dbcadb/src/hono-base.ts#L35
    handleHonoException(err, context) {
      const shouldHandleError = options.shouldHandleError || defaultShouldHandleError;

      if (!isHonoError(err)) {
        debugBuild.DEBUG_BUILD && core.debug.log("[Hono] Won't capture exception in `onError` because it's not a Hono error.", err);
        return;
      }

      if (shouldHandleError(err)) {
        if (context) {
          const activeSpan = core.getActiveSpan();
          const spanName = `${context.req.method} ${routePath(context)}`;

          if (activeSpan) {
            activeSpan.updateName(spanName);
            core.updateSpanName(core.getRootSpan(activeSpan), spanName);
          }

          core.getIsolationScope().setTransactionName(spanName);
        }

        core.captureException(err, { mechanism: { handled: false, type: 'auto.faas.hono.error_handler' } });
      } else {
        debugBuild.DEBUG_BUILD && core.debug.log('[Hono] Not capturing exception because `shouldHandleError` returned `false`.', err);
      }
    },
  };
}) ;

/**
 * Automatically captures exceptions caught with the `onError` handler in Hono.
 *
 * The integration is enabled by default.
 *
 * @example
 * integrations: [
 *   honoIntegration({
 *     shouldHandleError: (err) => true; // always capture exceptions in onError
 *   })
 * ]
 */
const honoIntegration = core.defineIntegration(_honoIntegration);

/**
 * Default function to determine if an error should be sent to Sentry
 *
 * 3xx and 4xx errors are not sent by default.
 */
function defaultShouldHandleError(error) {
  const statusCode = error?.status;
  // 3xx and 4xx errors are not sent by default.
  return statusCode ? statusCode >= 500 || statusCode <= 299 : true;
}

exports.getHonoIntegration = getHonoIntegration;
exports.honoIntegration = honoIntegration;
//# sourceMappingURL=hono.js.map
