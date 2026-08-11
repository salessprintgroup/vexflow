// Vexflow.app/Contents/MacOS/vexflow — the bundle's executable.
//
// All it does is run Contents/Resources/launcher.sh, which is where the real work
// still lives. The indirection is not tidiness; it is the only way to get a microphone
// dialog on some Macs.
//
// macOS decides who is responsible for a process from the image the kernel loads at
// exec time, and does not revise that decision when the process execs again. With a
// shell script as CFBundleExecutable the loaded image is /bin/bash, so every privacy
// request the app makes is attributed to /bin/bash — which has no bundle, no name and
// no usage description, and which macOS therefore never raises a consent dialog for.
// The request is answered "not determined" without asking anybody, so the onboarding
// window's microphone button appears to do nothing, permanently. Observed on macOS
// 13.7.8, where tccd logs the request as `AUTHREQ_SUBJECT: subject=/bin/bash`.
//
// Compiled, the loaded image is inside the bundle. The same request is then attributed
// to Vexflow.app, and macOS shows its own dialog carrying the sentence from
// Info.plist — in the system language, from the .lproj tables built alongside it.
//
// This is not a step towards freezing the app. What runs is still the readable Python
// in Contents/Resources/app, started by the readable shell script next to it; both can
// still be edited in place in an installed copy. The only thing that changed is which
// name macOS puts in the permission dialog.

#include <limits.h>
#include <mach-o/dyld.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

int main(void) {
    // Not argv[0]: launchd and LaunchServices are both entitled to put something else
    // there, and this has to be the path macOS actually loaded.
    char path[PATH_MAX];
    uint32_t size = sizeof(path);
    if (_NSGetExecutablePath(path, &size) != 0) {
        fprintf(stderr, "vexflow: executable path does not fit in PATH_MAX\n");
        return 1;
    }

    char resolved[PATH_MAX];
    if (realpath(path, resolved) == NULL) {
        perror("vexflow: cannot resolve my own path");
        return 1;
    }

    // .../Contents/MacOS/vexflow -> .../Contents, one component at a time. dirname()
    // would do it, but it returns static storage that the second call overwrites while
    // the first result is still being read.
    for (int i = 0; i < 2; i++) {
        char *slash = strrchr(resolved, '/');
        if (slash == NULL) {
            fprintf(stderr, "vexflow: %s is not inside a bundle\n", resolved);
            return 1;
        }
        *slash = '\0';
    }

    char script[PATH_MAX];
    if (snprintf(script, sizeof(script), "%s/Resources/launcher.sh", resolved)
            >= (int)sizeof(script)) {
        fprintf(stderr, "vexflow: bundle path is too long\n");
        return 1;
    }

    // No argument pass-through on purpose: LaunchServices adds -psn_0_… on some launch
    // paths, and bash would take it for a script to run.
    char *const args[] = {"/bin/bash", script, NULL};
    execv("/bin/bash", args);

    perror("vexflow: cannot start Resources/launcher.sh");
    return 127;
}
