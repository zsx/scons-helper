/* This file is used when compiling the source with MSVC .net or newer, but
 * linking against os supplied msvcr.dll instead of the compiler supplied one.
 */
#ifndef _MSVCRT_COMPAT_H_
#define _MSVCRT_COMPAT_H_

#ifdef MSVCRT_COMPAT_STAT
#include <sys/stat.h>

#ifdef _fstat /* will be defined to _fstat64i32 */
#undef _fstat
#endif

#ifdef _wstat /* _fstat64i32 */
#undef _wstat
#endif

#ifdef _stat
#undef _stat
#endif

#ifndef stat
#define stat(x, y) _stat(x, y)
#endif

#ifndef fstat
#define fstat(a,b) _fstat(a,b)
#endif
#endif /* MSVCRT_COMPAT_STAT */

#ifdef MSVCRT_COMPAT_IO
#include <io.h>

#ifdef _wfindfirst
#undef _wfindfirst
#endif

#ifdef _wfindnext
#undef _wfindnext
#endif

#ifdef _findfirst
#undef _findfirst
#endif

#ifdef _findnext
#undef _findnext
#endif
#endif /* MSVCRT_COMPAT_FIND */

#ifdef MSVCRT_COMPAT_SPRINTF
#include <stdio.h>
#include <stdarg.h>
#ifndef vsnprintf
#define vsnprintf(buf, size, fmt, ap) _vsnprintf(buf, size, fmt, ap)
#endif
#endif /* MSVCRT_COMPAT_SPRINTF */

#endif /* _MSVCRT_COMPAT_H_ */
