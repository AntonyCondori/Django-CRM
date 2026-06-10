import type { StackFrame } from '@sentry/core';
type StackFrameIteratee = (frame: StackFrame) => StackFrame;
interface RewriteFramesOptions {
    root?: string;
    prefix?: string;
    iteratee?: StackFrameIteratee;
}
export declare const customRewriteFramesIntegration: (options?: RewriteFramesOptions) => import("@sentry/core").Integration;
export declare const rewriteFramesIntegration: (options?: RewriteFramesOptions | undefined) => import("@sentry/core").Integration;
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
export declare function rewriteFramesIteratee(frame: StackFrame): StackFrame;
export {};
//# sourceMappingURL=rewriteFramesIntegration.d.ts.map