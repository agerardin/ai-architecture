"""
Copyright 2025 Antoine Gerardin

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from .event_bus import EventBus
from .redis_bus import RedisEventBus

def create_event_bus(provider: str = 'redis', **kwargs) -> EventBus:
    if provider == 'redis':
        return RedisEventBus(**kwargs)
    else:
        raise NotImplementedError(f"Provider {provider} not implemented.")
