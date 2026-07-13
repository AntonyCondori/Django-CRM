import { SEMANTIC_ATTRIBUTE_SENTRY_ORIGIN } from '@sentry/browser';
import { debug, startInactiveSpan } from '@sentry/core';
import { onMount, beforeUpdate, afterUpdate } from 'svelte';
import { DEBUG_BUILD } from './debug_build.js';

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
      DEBUG_BUILD &&
        debug.warn(
          "Cannot track component updates. This is likely because you're using Svelte 5 in Runes mode. Set `trackUpdates: false` in `withSentryConfig` or `trackComponent` to disable this warning.",
        );
    }
  }
}

function recordInitSpan(componentName) {
  const initSpan = startInactiveSpan({
    onlyIfParent: true,
    op: 'ui.svelte.init',
    name: componentName,
    attributes: { [SEMANTIC_ATTRIBUTE_SENTRY_ORIGIN]: 'auto.ui.svelte' },
  });

  onMount(() => {
    initSpan.end();
  });
}

function recordUpdateSpans(componentName) {
  let updateSpan;
  beforeUpdate(() => {
    updateSpan = startInactiveSpan({
      onlyIfParent: true,
      op: 'ui.svelte.update',
      name: componentName,
      attributes: { [SEMANTIC_ATTRIBUTE_SENTRY_ORIGIN]: 'auto.ui.svelte' },
    });
  });

  afterUpdate(() => {
    if (!updateSpan) {
      return;
    }
    updateSpan.end();
    updateSpan = undefined;
  });
}

export { trackComponent };
//# sourceMappingURL=performance.js.map
