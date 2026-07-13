Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });

const autoInstrument = require('./autoInstrument.js');
const detectAdapter = require('./detectAdapter.js');
const injectGlobalValues = require('./injectGlobalValues.js');
const sourceMaps = require('./sourceMaps.js');
const svelteConfig = require('./svelteConfig.js');

const DEFAULT_PLUGIN_OPTIONS = {
  autoUploadSourceMaps: true,
  autoInstrument: true,
  debug: false,
};

/**
 * Vite Plugins for the Sentry SvelteKit SDK, taking care of creating
 * Sentry releases and uploading source maps to Sentry.
 *
 * Sentry adds a few additional properties to your Vite config.
 * Make sure, it is registered before the SvelteKit plugin.
 */
async function sentrySvelteKit(options = {}) {
  const svelteConfig$1 = await svelteConfig.loadSvelteConfig();

  const mergedOptions = {
    ...DEFAULT_PLUGIN_OPTIONS,
    ...options,
    adapter: options.adapter || (await detectAdapter.detectAdapter(svelteConfig$1, options.debug)),
  };

  const sentryPlugins = [];

  if (mergedOptions.autoInstrument) {
    // TODO: Once tracing is promoted stable, we need to adjust this check!
    const kitTracingEnabled = !!svelteConfig$1.kit?.experimental?.tracing?.server;

    const pluginOptions = {
      load: true,
      serverLoad: true,
      ...(typeof mergedOptions.autoInstrument === 'object' ? mergedOptions.autoInstrument : {}),
    };

    sentryPlugins.push(
      autoInstrument.makeAutoInstrumentationPlugin({
        ...pluginOptions,
        debug: options.debug || false,
        // if kit-internal tracing is enabled, we only want to wrap and instrument client-side code.
        onlyInstrumentClient: kitTracingEnabled,
      }),
    );
  }

  const sentryVitePluginsOptions = generateVitePluginOptions(mergedOptions);

  if (mergedOptions.autoUploadSourceMaps) {
    // When source maps are enabled, we need to inject the output directory to get a correct
    // stack trace, by using this SDK's `rewriteFrames` integration.
    // This integration picks up the value.
    // TODO: I don't think this is technically correct. Either we always or never inject the output directory.
    // Stack traces shouldn't be different, depending on source maps config. With debugIds, we might not even
    // need to rewrite frames anymore.
    sentryPlugins.push(await injectGlobalValues.makeGlobalValuesInjectionPlugin(svelteConfig$1, mergedOptions));
  }

  if (sentryVitePluginsOptions) {
    const sentryVitePlugins = await sourceMaps.makeCustomSentryVitePlugins(sentryVitePluginsOptions, svelteConfig$1);
    sentryPlugins.push(...sentryVitePlugins);
  }

  return sentryPlugins;
}

/**
 * This function creates the options for the custom Sentry Vite plugin.
 * The options are derived from the Sentry SvelteKit plugin options, where the `_unstable` options take precedence.
 *
 * only exported for testing
 */
function generateVitePluginOptions(
  svelteKitPluginOptions,
) {
  let sentryVitePluginsOptions = null;

  // Bundle Size Optimizations
  if (svelteKitPluginOptions.bundleSizeOptimizations) {
    sentryVitePluginsOptions = {
      bundleSizeOptimizations: {
        ...svelteKitPluginOptions.bundleSizeOptimizations,
      },
    };
  }

  // todo(v11): remove deprecated options (Also from options type)

  // Source Maps
  if (svelteKitPluginOptions.autoUploadSourceMaps && process.env.NODE_ENV !== 'development') {
    const {
      // eslint-disable-next-line deprecation/deprecation
      unstable_sentryVitePluginOptions: deprecated_unstableSourceMapUploadOptions,
      ...deprecatedSourceMapUploadOptions
      // eslint-disable-next-line deprecation/deprecation
    } = svelteKitPluginOptions.sourceMapsUploadOptions || {};

    const {
      // eslint-disable-next-line @typescript-eslint/no-unused-vars,deprecation/deprecation
      sourceMapsUploadOptions: _filtered1,
      // eslint-disable-next-line @typescript-eslint/no-unused-vars
      unstable_sentryVitePluginOptions: _filtered2,
      // eslint-disable-next-line @typescript-eslint/no-unused-vars
      autoUploadSourceMaps: _filtered3,
      // eslint-disable-next-line @typescript-eslint/no-unused-vars
      autoInstrument: _filtered4,
      sentryUrl,
      ...newSvelteKitPluginOptions
    } = svelteKitPluginOptions;

    const { unstable_sentryVitePluginOptions } = svelteKitPluginOptions;

    sentryVitePluginsOptions = {
      ...(sentryVitePluginsOptions ? sentryVitePluginsOptions : {}),

      ...deprecatedSourceMapUploadOptions,
      ...newSvelteKitPluginOptions,

      url: sentryUrl,

      ...deprecated_unstableSourceMapUploadOptions,
      ...unstable_sentryVitePluginOptions,

      adapter: svelteKitPluginOptions.adapter,
      // override the plugin's debug flag with the one from the top-level options
      debug: svelteKitPluginOptions.debug,
    };

    // Handle sourcemaps options - merge deprecated and new, with new taking precedence
    if (
      // eslint-disable-next-line deprecation/deprecation
      deprecatedSourceMapUploadOptions.sourcemaps ||
      svelteKitPluginOptions.sourcemaps ||
      deprecated_unstableSourceMapUploadOptions?.sourcemaps ||
      unstable_sentryVitePluginOptions?.sourcemaps
    ) {
      sentryVitePluginsOptions.sourcemaps = {
        // eslint-disable-next-line deprecation/deprecation
        ...deprecatedSourceMapUploadOptions.sourcemaps,
        ...svelteKitPluginOptions.sourcemaps,
        // Also handle nested deprecated options from unstable plugin options
        ...deprecated_unstableSourceMapUploadOptions?.sourcemaps,
        ...unstable_sentryVitePluginOptions?.sourcemaps,
      };
    }

    // Handle release options - merge deprecated and new, with new taking precedence
    if (
      // eslint-disable-next-line deprecation/deprecation
      deprecatedSourceMapUploadOptions.release ||
      svelteKitPluginOptions.release ||
      deprecated_unstableSourceMapUploadOptions?.release ||
      unstable_sentryVitePluginOptions?.release
    ) {
      sentryVitePluginsOptions.release = {
        // eslint-disable-next-line deprecation/deprecation
        ...deprecatedSourceMapUploadOptions.release,
        ...svelteKitPluginOptions.release,
        // Also handle nested deprecated options from unstable plugin options
        ...deprecated_unstableSourceMapUploadOptions?.release,
        ...unstable_sentryVitePluginOptions?.release,
      };
    }
  }

  return sentryVitePluginsOptions;
}

exports.generateVitePluginOptions = generateVitePluginOptions;
exports.sentrySvelteKit = sentrySvelteKit;
//# sourceMappingURL=sentryVitePlugins.js.map
