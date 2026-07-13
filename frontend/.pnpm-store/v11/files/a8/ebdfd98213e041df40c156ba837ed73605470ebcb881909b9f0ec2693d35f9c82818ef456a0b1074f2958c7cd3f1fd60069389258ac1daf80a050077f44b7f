Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });

const core = require('@sentry/core');

// The SvelteKit default error handler just logs the error's stack trace to the console
// see: https://github.com/sveltejs/kit/blob/369e7d6851f543a40c947e033bfc4a9506fdc0a8/packages/kit/src/runtime/server/index.js#L43
function defaultErrorHandler({ error }) {
  // @ts-expect-error this conforms to the default implementation (including this ts-expect-error)
  // eslint-disable-next-line no-console
  core.consoleSandbox(() => console.error(error?.stack));
}

/**
 * Wrapper for the SvelteKit error handler that sends the error to Sentry.
 *
 * @param handleError The original SvelteKit error handler.
 */
function handleErrorWithSentry(handleError) {
  const errorHandler = handleError ?? defaultErrorHandler;

  return async (input) => {
    if (is4xxError(input)) {
      return errorHandler(input);
    }

    core.captureException(input.error, {
      mechanism: {
        type: 'auto.function.sveltekit.handle_error',
        handled: !!handleError,
      },
    });

    const platform = input.event.platform

;

    // Cloudflare workers have a `waitUntil` method on `ctx` that we can use to flush the event queue
    // We already call this in `wrapRequestHandler` from `sentryHandleInitCloudflare`
    // However, `handleError` can be invoked when wrapRequestHandler already finished
    // (e.g. when responses are streamed / returning promises from load functions)
    if (typeof platform?.context?.waitUntil === 'function') {
      await core.flushIfServerless({ cloudflareCtx: platform.context  });
    } else {
      await core.flushIfServerless();
    }

    return errorHandler(input);
  };
}

/**
 * When a page request fails because the page is not found, SvelteKit throws a "Not found" error.
 */
function is4xxError(input) {
  const { error, event, status } = input;

  // SvelteKit 2.0 offers a reliable way to check for a Not Found error:
  if (!!status && status >= 400 && status < 500) {
    return true;
  }

  // SvelteKit 1.x doesn't offer a reliable way to check for a Not Found error.
  // So we check the route id (shouldn't exist) and the raw stack trace
  // We can delete all of this below whenever we drop Kit 1.x support
  const hasNoRouteId = !event.route?.id;

  const rawStack =
    (error != null &&
      typeof error === 'object' &&
      'stack' in error &&
      typeof error.stack === 'string' &&
      error.stack) ||
    '';

  return hasNoRouteId && rawStack.startsWith('Error: Not found:');
}

exports.handleErrorWithSentry = handleErrorWithSentry;
//# sourceMappingURL=handleError.js.map
