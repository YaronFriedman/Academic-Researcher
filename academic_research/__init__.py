# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Academic_Research: Research advice, related literature finding, research area proposals, web knowledge access."""

import os
import threading

from deepchecks_llm_client.data_types import EnvType
from deepchecks_llm_client.otel import GoogleAdkIntegration
from dotenv import load_dotenv
from opentelemetry.sdk.trace import ReadableSpan, SpanProcessor

load_dotenv()


class SessionIdNormalizerProcessor(SpanProcessor):
    """Ensures all spans in the same trace share the root span's session.id."""

    def __init__(self):
        self._trace_session_map: dict[str, str] = {}
        self._lock = threading.Lock()

    def on_start(self, span, parent_context=None):
        trace_id = format(span.context.trace_id, '032x')
        session_id = None
        if hasattr(span, 'attributes') and span.attributes:
            session_id = span.attributes.get('session.id')

        with self._lock:
            if trace_id not in self._trace_session_map and session_id:
                self._trace_session_map[trace_id] = session_id
            elif trace_id in self._trace_session_map and session_id != self._trace_session_map[trace_id]:
                root_session = self._trace_session_map[trace_id]
                span._attributes = dict(span._attributes) if span._attributes else {}
                span._attributes['session.id'] = root_session

    def on_end(self, span: ReadableSpan):
        trace_id = format(span.context.trace_id, '032x')
        root_session = None
        with self._lock:
            root_session = self._trace_session_map.get(trace_id)

        if root_session and span.attributes and span.attributes.get('session.id') != root_session:
            if hasattr(span, '_attributes') and span._attributes is not None:
                span._attributes = dict(span._attributes)
                span._attributes['session.id'] = root_session

    def shutdown(self):
        pass

    def force_flush(self, timeout_millis=None):
        pass


try:
    tracer_provider = GoogleAdkIntegration().register_dc_exporter(
        host=os.environ["DEEPCHECKS_HOST"],
        api_key=os.environ["DEEPCHECKS_API_KEY"],
        app_name=os.environ["DEEPCHECKS_APP_NAME"],
        version_name=os.environ.get("DEEPCHECKS_VERSION_NAME", "v1"),
        env_type=EnvType.EVAL,
        log_to_console=True,
    )
    tracer_provider.add_span_processor(SessionIdNormalizerProcessor())
except Exception as e:
    print(f"Warning: Deepchecks instrumentation failed: {e}")

from . import agent  # noqa: E402 — must import after instrumentation is registered
