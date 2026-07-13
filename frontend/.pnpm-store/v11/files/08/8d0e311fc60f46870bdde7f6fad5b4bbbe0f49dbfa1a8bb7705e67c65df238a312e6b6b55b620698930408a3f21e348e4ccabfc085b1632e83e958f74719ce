Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });

const browser = require('@sentry/browser');
const core = require('@sentry/core');
const svelte = require('svelte');
const debug_build = require('./debug_build.js');

const defaultTrackComponentOptions

 = {
  trackInit: true,
  trackUpdates: false,
};

/**
 * Tracks the Svelte component's initialization and mounting operation as well as
 * updates and records them as spans.
 *
 * This function is injected automatically into your Svelte components' code
 * if you are using the withSentryConfig wrapper.
 *
 * Alternatively, you can call it yourself if you don't want to use the preprocessor.
 */
function trackComponent(options) {
  const mergedOptions = { ...defaultTrackComponentOptions, ...options };

  const customComponentName = mergedOptions.componentName;

  const componentName = `<${customComponentName || 'Svelte Component'}>`;

  if (mergedOptions.trackInit) {
    recordInitSpan(componentName);
  }

  if (mergedOptions.trackUpdates) {
    try {
      recordUpdateSpans(componentName);
    } catch {
      debug_build.DEBUG_BUILD &&
        core.debug.warn(
          "Cannot track component updates. This is likely because you're using Svelte 5 in Runes mode. Set `trackUpdates: false` in `withSentryConfig` or `trackComponent` to disable this warning.",
        );
    }
  }
}

function recordInitSpan(componentName) {
  const initSpan = core.startInactiveSpan({
    onlyIfParent: true,
    op: 'ui.svelte.init',
    name: componentName,
    attributes: { [browser.SEMANTIC_ATTRIBUTE_SENTRY_ORIGIN]: 'auto.ui.svelte' },
  });

  svelte.onMount(() => {
    initSpan.end();
  });
}

function recordUpdateSpans(componentName) {
  let updateSpan;
  svelte.beforeUpdate(() => {
    updateSpan = core.startInactiveSpan({
      onlyIfParent: true,
      op: 'ui.svelte.update',
      name: componentName,
      attributes: { [browser.SEMANTIC_ATTRIBUTE_SENTRY_ORIGIN]: 'auto.ui.svelte' },
    });
  });

  svelte.afterUpdate(() => {
    if (!updateSpan) {
      return;
    }
    updateSpan.end();
    updateSpan = undefined;
  });
}

exports.trackComponent = trackComponent;
//# sourceMappingURL=performance.js.map
