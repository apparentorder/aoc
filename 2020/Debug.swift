//
// Swift will *always* evaluate a string expression. This means that the
// performance of debug("foo \(bar)") would normally mirror the complexity of
// describing `bar`. If this is a comlex and/or nested structure, the
// performance would be abysmal, especially when used e.g. in a
// high-iteration loop.
//
// This is true even if the debug() function body is completely empty
// and is optimized away by the -O flag. In other words: This performance
// impact would affect execution without debug output just as well.
//
// Using @autoclosure solves this by automatically wrapping the argument in
// a closure, so it won't be evaluated before it is actually printed.
//
// See also:
// https://www.swiftbysundell.com/articles/using-autoclosure-when-designing-swift-apis/
// (with a thank you to #swift-lang@freenode).
//

func debug(_ message: @autoclosure () -> String) {
	#if DEBUG
	guard debugEnabled else { return }
	print(message())
	#endif
}

func debug<T>(_ s: T) {
	#if DEBUG
	debug(String(describing: s))
	#endif
}

