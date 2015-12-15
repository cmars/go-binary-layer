# go-binary-layer

This layer was originally designed for installing services developed in Go.

# Using go-binary in your charm

## Setup

Add `layer:go-binary` to your `layer.yaml`.

Add a configuration file, `go-binary.yaml`:

```
binary: <name of binary>
args: <command line arguments (not including the binary name)
```

For example:

```
binary: hockeypuck
args: --config /etc/hockeypuck/hockeypuck.conf
```

will result in an upstart job that executes '/usr/bin/hockeypuck --config /etc/hockeypuck/hockeypuck.conf`.

Finally, copy the statically-compiled binary (same name as specified in
`go-binary.yaml`) to files/<binary name>. Technically, it doesn't *have* to be
a Go-compiled binary, but that's the intended purpose.

# Install and upgrade hooks

This layer will:

- Install the provided binary to /usr/bin.
- Create an upstart job for the binary, that automatically starts it. Service
  name is the same as the binary name.

# Reactive behavior

## States Consumed

This layer consumes the following states. The state is removed once it is handled.

### go-binary.start

Will start the service, or restart it if already running.

### go-binary.stop

Will stop the service, if it was running. If not, it has no effect.

## States Provided

This layer provides the following states. They should be removed once they are handled by your layer.

### go-binary.available

Is set once the service is installed.

### go-binary.started

Is set when the service is started.

# TODO

- Support for multiple release versions.
- User separation between files and running process.

---

Copyright 2015 Canonical, Ltd.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
