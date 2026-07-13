Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });

const core = require('@sentry/core');
const MagicString = require('magic-string');
const svelteConfig = require('./svelteConfig.js');

const VIRTUAL_GLOBAL_VALUES_FILE = '\0sentry-inject-global-values-file';

/**
 * @returns code that injects @param globalSentryValues into the global object.
 */
function getGlobalValueInjectionCode(globalSentryValues) {
  if (Object.keys(globalSentryValues).length === 0) {
    return '';
  }

  const injectedValuesCode = Object.entries(globalSentryValues)
    .map(([key, value]) => `globalThis["${key}"] = ${JSON.stringify(value)};`)
    .join('\n');

  return `${injectedValuesCode}\n`;
}

/**
 * Injects SvelteKit app configuration values the svelte.config.js into the
 * server's global object so that the SDK can pick up the information at runtime
 */
async function makeGlobalValuesInjectionPlugin(
  svelteConfig$1,
  options,
) {
  const { adapter = 'other', debug = false } = options;

  const serverHooksFile = svelteConfig.getHooksFileName(svelteConfig$1, 'server');
  const adapterOutputDir = await svelteConfig.getAdapterOutputDir(svelteConfig$1, adapter);

  const globalSentryValues = {
    __sentry_sveltekit_output_dir: adapterOutputDir,
  };

  if (debug) {
    // eslint-disable-next-line no-console
    console.log('[Sentry SvelteKit] Global values:', globalSentryValues);
  }

  // oxlint-disable-next-line sdk/no-regexp-constructor -- not end user input + escaped anyway
  const hooksFileRegexp = new RegExp(`/${core.escapeStringForRegex(serverHooksFile)}(.(js|ts|mjs|mts))?`);

  return {
    name: 'sentry-sveltekit-global-values-injection-plugin',
    resolveId: (id, _importer, _ref) => {
      if (id === VIRTUAL_GLOBAL_VALUES_FILE) {
        return {
          id: VIRTUAL_GLOBAL_VALUES_FILE,
          external: false,
          moduleSideEffects: true,
        };
      }
      return null;
    },

    load: id => {
      if (id === VIRTUAL_GLOBAL_VALUES_FILE) {
        return {
          code: getGlobalValueInjectionCode(globalSentryValues),
        };
      }
      return null;
    },

    transform: async (code, id) => {
      const isServerEntryFile = /instrumentation\.server\./.test(id) || hooksFileRegexp.test(id);

      if (isServerEntryFile) {
        if (debug) {
          // eslint-disable-next-line no-console
          console.log('[Global Values Plugin] Injecting global values into', id);
        }
        const ms = new MagicString.default(code);
        ms.append(`\n; import "${VIRTUAL_GLOBAL_VALUES_FILE}";\n`);
        return {
          code: ms.toString(),
          map: ms.generateMap({ hires: true }),
        };
      }

      return null;
    },
  };
}

exports.VIRTUAL_GLOBAL_VALUES_FILE = VIRTUAL_GLOBAL_VALUES_FILE;
exports.getGlobalValueInjectionCode = getGlobalValueInjectionCode;
exports.makeGlobalValuesInjectionPlugin = makeGlobalValuesInjectionPlugin;
//# sourceMappingURL=injectGlobalValues.js.map
