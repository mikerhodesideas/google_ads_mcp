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

"""The server for the Google Ads API MCP."""

from ads_mcp.coordinator import mcp

from ads_mcp.tools import api
from ads_mcp.tools import docs
from scripts.generate_views import update_views_yaml


tools = [api, docs]


def main():
  """Initializes and runs the MCP server."""
  update_views_yaml()  # Check and update docs resource
  mcp.run()  # Initialize and run the server


if __name__ == "__main__":
  main()
