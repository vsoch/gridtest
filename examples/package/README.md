# Package Testing

You don't necessarily need to write tests just for local files or modules!
Gridtest also works to generate tests for modules installed with your Python.
This provides a quick example for that. First, generate a testing file:

```bash
gridtest generate requests gridtest.yml --skip-classes
```

Note that we just want to test the simple requests functions, so we are 
skipping classes. If I wanted to include private functions:

```bash
$ gridtest generate --include-private --skip-classes requests gridtest.yml
```

In the case of requests, I don't really want to test more of the complex
functionlity, but just the functions that I might need to use. Thus,  
I can then open the file and just delete those chunks. I'd then
update the file to customize it with my tests, meaning that I change this:

```yaml
requests:
  filename: /home/vanessa/anaconda3/lib/python3.7/site-packages/requests/__init__.py
  tests:
    _internal_utils.to_native_string:
    - args:
        encoding: null
        string: ascii
    _internal_utils.unicode_is_ascii:
    - args:
        u_string: null
    adapters._basic_auth_str:
    - args:
        password: null
        username: null
    adapters.extract_cookies_to_jar:
    - args:
        jar: null
        request: null
        response: null
    adapters.extract_zipped_paths:
    - args:
        path: null
    adapters.get_auth_from_url:
    - args:
        url: null
    adapters.get_encoding_from_headers:
    - args:
        headers: null
    adapters.prepend_scheme_if_needed:
    - args:
        new_scheme: null
        url: null
    adapters.select_proxy:
    - args:
        proxies: null
        url: null
    adapters.urldefragauth:
    - args:
        url: null
    auth.parse_dict_header:
    - args:
        value: null
    cookies._copy_cookie_jar:
    - args:
        jar: null
    cookies.cookiejar_from_dict:
    - args:
        cookie_dict: null
        cookiejar: true
        overwrite: null
    cookies.create_cookie:
    - args:
        name: null
        value: null
    cookies.get_cookie_header:
    - args:
        jar: null
        request: null
    cookies.merge_cookies:
    - args:
        cookiejar: null
        cookies: null
    cookies.morsel_to_cookie:
    - args:
        morsel: null
    cookies.remove_cookie_by_name:
    - args:
        cookiejar: null
        domain: null
        name: null
        path: null
    hooks.default_hooks:
    - args: {}
    hooks.dispatch_hook:
    - args:
        hook_data: null
        hooks: null
        key: null
    models.check_header_validity:
    - args:
        header: null
    models.guess_filename:
    - args:
        obj: null
    models.guess_json_utf:
    - args:
        data: null
    models.iter_slices:
    - args:
        slice_length: null
        string: null
    models.parse_header_links:
    - args:
        value: null
    models.requote_uri:
    - args:
        uri: null
    models.stream_decode_response_unicode:
    - args:
        iterator: null
        r: null
    models.super_len:
    - args:
        o: null
    models.to_key_val_list:
    - args:
        value: null
    requests._check_cryptography:
    - args:
        cryptography_version: null
    requests.check_compatibility:
    - args:
        chardet_version: null
        urllib3_version: null
    requests.delete:
    - args:
        url: null
    requests.get:
    - args:
        params: null
        url: null
    requests.head:
    - args:
        url: null
    requests.options:
    - args:
        url: null
    requests.patch:
    - args:
        data: null
        url: null
    requests.post:
    - args:
        data: null
        json: null
        url: null
    requests.put:
    - args:
        data: null
        url: null
    requests.request:
    - args:
        method: null
        url: null
    requests.session:
    - args: {}
    sessions.default_headers:
    - args: {}
    sessions.get_environ_proxies:
    - args:
        no_proxy: null
        url: null
    sessions.get_netrc_auth:
    - args:
        raise_errors: null
        url: false
    sessions.merge_hooks:
    - args:
        dict_class: null
        request_hooks: &id001 !!python/name:collections.OrderedDict ''
        session_hooks: null
    sessions.merge_setting:
    - args:
        dict_class: null
        request_setting: *id001
        session_setting: null
    sessions.rewind_body:
    - args:
        prepared_request: null
    sessions.should_bypass_proxies:
    - args:
        no_proxy: null
        url: null
    status_codes._init:
    - args: {}
    utils._parse_content_type_header:
    - args:
        header: null
    utils.add_dict_to_cookiejar:
    - args:
        cj: null
        cookie_dict: null
    utils.address_in_network:
    - args:
        ip: null
        net: null
    utils.default_user_agent:
    - args:
        name: python-requests
    utils.dict_from_cookiejar:
    - args:
        cj: null
    utils.dict_to_sequence:
    - args:
        d: null
    utils.dotted_netmask:
    - args:
        mask: null
    utils.from_key_val_list:
    - args:
        value: null
    utils.get_encodings_from_content:
    - args:
        content: null
    utils.get_unicode_from_response:
    - args:
        r: null
    utils.is_ipv4_address:
    - args:
        string_ip: null
    utils.is_valid_cidr:
    - args:
        string_network: null
    utils.parse_list_header:
    - args:
        value: null
    utils.unquote_header_value:
    - args:
        is_filename: null
        value: false
    utils.unquote_unreserved:
    - args:
        uri: null
```

to this:

```yaml
requests:
  filename: /home/vanessa/anaconda3/lib/python3.7/site-packages/requests/__init__.py
  tests:
    requests.api.get:
    - args:
        params: null
        url: https://google.com
      isinstance: Response
    requests.api.head:
    - args:
        url: https://google.com
      istrue: "self.result.status_code == 301"
    requests.api.options:
    - args:
        url: https://google.com
```

This recipe also shows a good example of how to check for an instance type.
The string "Response" should be given if I check the `type(result).__name__`
for the result. Also notice the `istrue` statement isn't targeting a `{{ result }}`
template that can be converted to a string and evaluated, but rather the GridTest
instance directly (self.result) and more specifically, the status_code attribute.

## Running Tests

And then run your tests:

```bash
$ gridtest test
[3/3] |===================================| 100.0% 
Name                           Status                         Summary                       
________________________________________________________________________________________________________________________
requests.api.get.0             success                        isinstance Response           
requests.api.head.0            success                        istrue self.result.status_code == 301
requests.api.options.0         success                                                      

3/3 tests passed
```
