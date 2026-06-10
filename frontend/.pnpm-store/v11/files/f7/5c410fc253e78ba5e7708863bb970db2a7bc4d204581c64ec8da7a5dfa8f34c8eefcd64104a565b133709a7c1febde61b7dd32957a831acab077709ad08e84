const WRAPPED_MODULE_SUFFIX = '?sentry-auto-wrap';

/**
 * Get route.id from a load event without triggering SvelteKit's route proxy
 * (which would cause unwanted invalidations). Uses `untrack` when available (SvelteKit 2+),
 * otherwise falls back to getOwnPropertyDescriptor for SvelteKit 1.x.
 */
function getRouteId(event) {
  if (typeof event.untrack === 'function') {
    return event.untrack(() => event.route?.id ?? undefined);
  }

  const route = event.route;
  if (!route) {
    return;
  }

  const descriptor = Object.getOwnPropertyDescriptor(route, 'id');
  const fromDescriptor = descriptor?.value ;

  if (fromDescriptor !== undefined && fromDescriptor !== null) {
    return fromDescriptor;
  }

  return;
}

/**
 * Determines if a thrown "error" is a Redirect object which SvelteKit users can throw to redirect to another route
 * see: https://kit.svelte.dev/docs/modules#sveltejs-kit-redirect
 * @param error the potential redirect error
 */
function isRedirect(error) {
  if (error == null || typeof error !== 'object') {
    return false;
  }
  const hasValidLocation = 'location' in error && typeof error.location === 'string';
  const hasValidStatus =
    'status' in error && typeof error.status === 'number' && error.status >= 300 && error.status <= 308;
  return hasValidLocation && hasValidStatus;
}

/**
 * Determines if a thrown "error" is a HttpError
 */
function isHttpError(err) {
  return typeof err === 'object' && err !== null && 'status' in err && 'body' in err;
}

export { WRAPPED_MODULE_SUFFIX, getRouteId, isHttpError, isRedirect };
//# sourceMappingURL=utils.js.map
