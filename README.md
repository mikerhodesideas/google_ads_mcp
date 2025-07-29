# Google Ads MCP server

Google Ads MCP Server is a specific implementation of the MCP that allows LLMs like Gemini to directly interact with Google Ads data.

## Installation

1.  **:**

    This project uses `uv` for dependency management. Install `uv` from the official website.

2.  **Install dependencies:**

    After installed `uv`, you can install the dependencies with the following command:

    ```bash
    uv pip sync
    ```

3.  **Configure Google Ads API credentials:**

    This tool requires you to have a `google-ads.yaml` file with your Google Ads API credentials. By default, the application will look for this file in your home directory.

    If you don't have one, you can generate it by running the following example from the `google-ads-python` library:
    [authentication example](https://github.com/googleads/google-ads-python/blob/main/examples/authentication/generate_user_credentials.py)

    Make sure your `google-ads.yaml` file contains the following keys:
    - `client_id`
    - `client_secret`
    - `refresh_token`
    - `developer_token`
    - `login_customer_id` (optional, but recommended)


## Usage

To start the server, run the following command:

```bash
uv run -m ads_mcp.server
```

The server will start and be ready to accept requests.

## Gemini CLI Usage

Once the server is running, you can interact with it using the Gemini CLI.

Here is a reference config:

```json
{
// Other configs...
"mcpServers": {
    "GoogleAds": {
      "command": "uv",
      "args": ["run","--directory","[DIRECTORY]", "ads-mcp/server.py"],
      "cwd": "",
      "timeout": 30000,
      "trust": false,
      "includeTools":[""]
    }
  }
}
```

## Contributing

We welcome contributions! Please see our [CONTRIBUTING.md](CONTRIBUTING.md) guide for details.

## License

AdsPort is open-source software licensed under the [APACHE-2.0 License](LICENSE).

## Contact

If you have any questions, suggestions, or feedback, please feel free to open an issue or contact us at [adsport@google.com].

Let us help you elevate your advertising agency to new heights with AdsPort!

## Disclaimer

Copyright Google LLC. Supported by Google LLC and/or its affiliate(s). This solution, including any related sample code or data, is made available on an “as is,” “as available,” and “with all faults” basis, solely for illustrative purposes, and without warranty or representation of any kind. This solution is experimental, unsupported and provided solely for your convenience. Your use of it is subject to your agreements with Google, as applicable, and may constitute a beta feature as defined under those agreements.  To the extent that you make any data available to Google in connection with your use of the solution, you represent and warrant that you have all necessary and appropriate rights, consents and permissions to permit Google to use and process that data.  By using any portion of this solution, you acknowledge, assume and accept all risks, known and unknown, associated with its usage and any processing of data by Google, including with respect to your deployment of any portion of this solution in your systems, or usage in connection with your business, if at all. With respect to the entrustment of personal information to Google, you will verify that the established system is sufficient by checking Google's privacy policy and other public information, and you agree that no further information will be provided by Google.
