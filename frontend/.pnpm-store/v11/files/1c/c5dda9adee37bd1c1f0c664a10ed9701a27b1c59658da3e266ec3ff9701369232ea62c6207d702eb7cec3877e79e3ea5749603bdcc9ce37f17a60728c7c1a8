Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });

const core = require('@sentry/core');
const utils = require('../../common/utils.js');

const customRewriteFramesIntegration = ((options) => {
  return core.rewriteFramesIntegration({
    iteratee: rewriteFramesIteratee,
    ...options,
  });
}) ;

const rewriteFramesIntegration = core.defineIntegration(customRewriteFramesIntegration);

/**
 * A custom iteratee function for the `RewriteFrames` integration.
 *
 * Does the same as the default iteratee, but also removes the `module` property from the
 * frame to improve issue grouping.
 *
 * For some reason, our stack trace processing pipeline isn't able to resolve the bundled
 * module name to the original file name correctly, leading to individual error groups for
 * each module. Removing the `module` field makes the grouping algorithm fall back to the
 * `filename` field, which is correctly resolved and hence grouping works as expected.
 *
 * Exported for tests only.
 */
function rewriteFramesIteratee(frame) {
  if (!frame.filename) {
    return frame;
  }
  const globalWithSentryValues = core.GLOBAL_OBJ;
  const svelteKitBuildOutDir = globalWithSentryValues.__sentry_sveltekit_output_dir;
  const prefix = 'app:///';

  // Check if the frame filename begins with `/` or a Windows-style prefix such as `C:\`
  const isWindowsFrame = /^[a-zA-Z]:\\/.test(frame.filename);
  const startsWithSlash = /^\//.test(frame.filename);
  if (isWindowsFrame || startsWithSlash) {
    const filename = isWindowsFrame
      ? frame.filename
          .replace(/^[a-zA-Z]:/, '') // remove Windows-style prefix
          .replace(/\\/g, '/') // replace all `\\` instances with `/`
      : frame.filename;

    let strippedFilename;
    if (svelteKitBuildOutDir) {
      strippedFilename = filename.replace(
        // oxlint-disable-next-line sdk/no-regexp-constructor -- not end user input + escaped anyway
        new RegExp(`^.*${core.escapeStringForRegex(core.join(svelteKitBuildOutDir, 'server'))}/`),
        '',
      );
    } else {
      strippedFilename = core.basename(filename);
    }
    frame.filename = `${prefix}${strippedFilename}`;
  }

  delete frame.module;

  // In dev-mode, the WRAPPED_MODULE_SUFFIX is still present in the frame's file name.
  // We need to remove it to make sure that the frame's filename matches the actual file
  if (frame.filename.endsWith(utils.WRAPPED_MODULE_SUFFIX)) {
    frame.filename = frame.filename.slice(0, -utils.WRAPPED_MODULE_SUFFIX.length);
  }

  return frame;
}

exports.customRewriteFramesIntegration = customRewriteFramesIntegration;
exports.rewriteFramesIntegration = rewriteFramesIntegration;
exports.rewriteFramesIteratee = rewriteFramesIteratee;
//# sourceMappingURL=rewriteFramesIntegration.js.map
