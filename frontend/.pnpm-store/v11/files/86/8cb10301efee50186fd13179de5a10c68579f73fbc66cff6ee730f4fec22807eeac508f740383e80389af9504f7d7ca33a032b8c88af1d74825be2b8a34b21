Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });

const core = require('@sentry/core');
const svelte = require('@sentry/svelte');
const stores = require('$app/stores');

/**
 * A custom `BrowserTracing` integration for SvelteKit.
 */
function browserTracingIntegration(
  options = {},
) {
  const integration = {
    ...svelte.browserTracingIntegration({
      ...options,
      instrumentNavigation: false,
      instrumentPageLoad: false,
    }),
  };

  return {
    ...integration,
    afterAllSetup: client => {
      integration.afterAllSetup(client);

      if (options.instrumentPageLoad !== false) {
        _instrumentPageload(client);
      }

      if (options.instrumentNavigation !== false) {
        _instrumentNavigations(client);
      }
    },
  };
}

function _instrumentPageload(client) {
  const initialPath = svelte.WINDOW.location?.pathname;

  const pageloadSpan = svelte.startBrowserTracingPageLoadSpan(client, {
    name: initialPath,
    op: 'pageload',
    attributes: {
      [core.SEMANTIC_ATTRIBUTE_SENTRY_ORIGIN]: 'auto.pageload.sveltekit',
      [core.SEMANTIC_ATTRIBUTE_SENTRY_SOURCE]: 'url',
    },
  });
  if (!pageloadSpan) {
    return;
  }

  // TODO(v11): require svelte 5 or newer to switch to `page` from `$app/state`
  // eslint-disable-next-line deprecation/deprecation
  stores.page.subscribe(page => {
    if (!page) {
      return;
    }

    const routeId = page.route?.id;

    if (routeId) {
      pageloadSpan.updateName(routeId);
      pageloadSpan.setAttribute(core.SEMANTIC_ATTRIBUTE_SENTRY_SOURCE, 'route');
      svelte.getCurrentScope().setTransactionName(routeId);
    }
  });
}

/**
 * Use the `navigating` store to start a transaction on navigations.
 */
function _instrumentNavigations(client) {
  let routingSpan;

  // TODO(v11): require svelte 5 or newer to switch to `navigating` from `$app/state`
  // eslint-disable-next-line deprecation/deprecation
  stores.navigating.subscribe(navigation => {
    if (!navigation) {
      // `navigating` emits a 'null' value when the navigation is completed.
      // So in this case, we can finish the routing span. If the span was an idle span,
      // it will finish automatically and if it was user-created users also need to finish it.
      if (routingSpan) {
        routingSpan.end();
        routingSpan = undefined;
      }
      return;
    }

    const from = navigation.from;
    const to = navigation.to;

    // for the origin we can fall back to window.location.pathname because in this emission, it still is set to the origin path
    const rawRouteOrigin = from?.url.pathname || svelte.WINDOW.location?.pathname;

    const rawRouteDestination = to?.url.pathname;

    // We don't want to create transactions for navigations of same origin and destination.
    // We need to look at the raw URL here because parameterized routes can still differ in their raw parameters.
    if (rawRouteOrigin === rawRouteDestination) {
      return;
    }

    const parameterizedRouteOrigin = from?.route.id;
    const parameterizedRouteDestination = to?.route.id;

    if (routingSpan) {
      // If a routing span is still open from a previous navigation, we finish it.
      // This is important for e.g. redirects when a new navigation root span finishes
      // the first root span. If we don't `.end()` the previous span, it will get
      // status 'cancelled' which isn't entirely correct.
      routingSpan.end();
    }

    const navigationInfo = {
      //  `navigation.type` denotes the origin of the navigation. e.g.:
      //   - link (clicking on a link)
      //   - goto (programmatic via goto() or redirect())
      //   - popstate (back/forward navigation)
      'sentry.sveltekit.navigation.type': navigation.type,
      'sentry.sveltekit.navigation.from': parameterizedRouteOrigin || undefined,
      'sentry.sveltekit.navigation.to': parameterizedRouteDestination || undefined,
    };

    svelte.startBrowserTracingNavigationSpan(client, {
      name: parameterizedRouteDestination || rawRouteDestination || 'unknown',
      op: 'navigation',
      attributes: {
        [core.SEMANTIC_ATTRIBUTE_SENTRY_ORIGIN]: 'auto.navigation.sveltekit',
        [core.SEMANTIC_ATTRIBUTE_SENTRY_SOURCE]: parameterizedRouteDestination ? 'route' : 'url',
        ...navigationInfo,
      },
    });

    routingSpan = svelte.startInactiveSpan({
      op: 'ui.sveltekit.routing',
      name: 'SvelteKit Route Change',
      attributes: {
        [core.SEMANTIC_ATTRIBUTE_SENTRY_ORIGIN]: 'auto.ui.sveltekit',
        ...navigationInfo,
      },
      onlyIfParent: true,
    });
  });
}

exports.browserTracingIntegration = browserTracingIntegration;
//# sourceMappingURL=browserTracingIntegration.js.map
