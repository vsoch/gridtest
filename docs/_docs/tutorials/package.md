---
title: Package Tutorial
category: Tutorials
permalink: /tutorials/package/index.html
order: 5
---

This tutorial covers writing gridtests for a specific package of interest,
such as the `requests` module that might already be installed in your python
site-packages. If you haven't [installed]({{ site.baseurl }}/install/) gridtest, you should do this first.

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
$ gridtest generate --include-private --skip-private requests gridtest.yml
```

In the case of requests, I don't really want to test more of the complex
functionlity, but just the functions that I might need to use. Thus,  
I can then open the file and just delete those chunks. I'd then
update the file to customize it with my tests, meaning that I change this:

```yaml
requests:
  filename: /home/vanessa/anaconda3/lib/python3.7/site-packages/requests/__init__.py
  requests.adapters.extract_cookies_to_jar:
  - args:
      jar: null
      request: null
      response: null
  requests.adapters.extract_zipped_paths:
  - args:
      path: null
  requests.adapters.get_auth_from_url:
  - args:
      url: null
  requests.adapters.get_encoding_from_headers:
  - args:
      headers: null
  requests.adapters.prepend_scheme_if_needed:
  - args:
      new_scheme: null
      url: null
  requests.adapters.select_proxy:
  - args:
      proxies: null
      url: null
  requests.adapters.urldefragauth:
  - args:
      url: null
  requests.api.delete:
  - args:
      url: null
  requests.api.get:
  - args:
      params: null
      url: null
  requests.api.head:
  - args:
      url: null
  requests.api.options:
  - args:
      url: null
  requests.api.patch:
  - args:
      data: null
      url: null
  requests.api.post:
  - args:
      data: null
      json: null
      url: null
  requests.api.put:
  - args:
      data: null
      url: null
  requests.api.request:
  - args:
      method: null
      url: null
  requests.auth.extract_cookies_to_jar:
  - args:
      jar: null
      request: null
      response: null
  requests.auth.parse_dict_header:
  - args:
      value: null
  requests.auth.to_native_string:
  - args:
      encoding: null
      string: ascii
  requests.cookies.cookiejar_from_dict:
  - args:
      cookie_dict: null
      cookiejar: true
      overwrite: null
  requests.cookies.create_cookie:
  - args:
      name: null
      value: null
  requests.cookies.extract_cookies_to_jar:
  - args:
      jar: null
      request: null
      response: null
  requests.cookies.get_cookie_header:
  - args:
      jar: null
      request: null
  requests.cookies.merge_cookies:
  - args:
      cookiejar: null
      cookies: null
  requests.cookies.morsel_to_cookie:
  - args:
      morsel: null
  requests.cookies.remove_cookie_by_name:
  - args:
      cookiejar: null
      domain: null
      name: null
      path: null
  requests.cookies.to_native_string:
  - args:
      encoding: null
      string: ascii
  requests.hooks.default_hooks:
  - args: {}
  requests.hooks.dispatch_hook:
  - args:
      hook_data: null
      hooks: null
      key: null
  requests.models.check_header_validity:
  - args:
      header: null
  requests.models.cookiejar_from_dict:
  - args:
      cookie_dict: null
      cookiejar: true
      overwrite: null
  requests.models.default_hooks:
  - args: {}
  requests.models.get_auth_from_url:
  - args:
      url: null
  requests.models.get_cookie_header:
  - args:
      jar: null
      request: null
  requests.models.guess_filename:
  - args:
      obj: null
  requests.models.guess_json_utf:
  - args:
      data: null
  requests.models.iter_slices:
  - args:
      slice_length: null
      string: null
  requests.models.parse_header_links:
  - args:
      value: null
  requests.models.requote_uri:
  - args:
      uri: null
  requests.models.stream_decode_response_unicode:
  - args:
      iterator: null
      r: null
  requests.models.super_len:
  - args:
      o: null
  requests.models.to_key_val_list:
  - args:
      value: null
  requests.models.to_native_string:
  - args:
      encoding: null
      string: ascii
  requests.models.unicode_is_ascii:
  - args:
      u_string: null
  requests.requests.check_compatibility:
  - args:
      chardet_version: null
      urllib3_version: null
  requests.requests.delete:
  - args:
      url: null
  requests.requests.get:
  - args:
      params: null
      url: null
  requests.requests.head:
  - args:
      url: null
  requests.requests.options:
  - args:
      url: null
  requests.requests.patch:
  - args:
      data: null
      url: null
  requests.requests.post:
  - args:
      data: null
      json: null
      url: null
  requests.requests.put:
  - args:
      data: null
      url: null
  requests.requests.request:
  - args:
      method: null
      url: null
  requests.requests.session:
  - args: {}
  requests.sessions.cookiejar_from_dict:
  - args:
      cookie_dict: null
      cookiejar: true
      overwrite: null
  requests.sessions.default_headers:
  - args: {}
  requests.sessions.default_hooks:
  - args: {}
  requests.sessions.dispatch_hook:
  - args:
      hook_data: null
      hooks: null
      key: null
  requests.sessions.extract_cookies_to_jar:
  - args:
      jar: null
      request: null
      response: null
  requests.sessions.get_auth_from_url:
  - args:
      url: null
  requests.sessions.get_environ_proxies:
  - args:
      no_proxy: null
      url: null
  requests.sessions.get_netrc_auth:
  - args:
      raise_errors: null
      url: false
  requests.sessions.merge_cookies:
  - args:
      cookiejar: null
      cookies: null
  requests.sessions.merge_hooks:
  - args:
      dict_class: null
      request_hooks: &id001 !!python/name:collections.OrderedDict ''
      session_hooks: null
  requests.sessions.merge_setting:
  - args:
      dict_class: null
      request_setting: *id001
      session_setting: null
  requests.sessions.requote_uri:
  - args:
      uri: null
  requests.sessions.rewind_body:
  - args:
      prepared_request: null
  requests.sessions.session:
  - args: {}
  requests.sessions.should_bypass_proxies:
  - args:
      no_proxy: null
      url: null
  requests.sessions.to_key_val_list:
  - args:
      value: null
  requests.sessions.to_native_string:
  - args:
      encoding: null
      string: ascii
  requests.utils.add_dict_to_cookiejar:
  - args:
      cj: null
      cookie_dict: null
  requests.utils.address_in_network:
  - args:
      ip: null
      net: null
  requests.utils.check_header_validity:
  - args:
      header: null
  requests.utils.cookiejar_from_dict:
  - args:
      cookie_dict: null
      cookiejar: true
      overwrite: null
  requests.utils.default_headers:
  - args: {}
  requests.utils.default_user_agent:
  - args:
      name: python-requests
  requests.utils.dict_from_cookiejar:
  - args:
      cj: null
  requests.utils.dict_to_sequence:
  - args:
      d: null
  requests.utils.dotted_netmask:
  - args:
      mask: null
  requests.utils.extract_zipped_paths:
  - args:
      path: null
  requests.utils.from_key_val_list:
  - args:
      value: null
  requests.utils.get_auth_from_url:
  - args:
      url: null
  requests.utils.get_encoding_from_headers:
  - args:
      headers: null
  requests.utils.get_encodings_from_content:
  - args:
      content: null
  requests.utils.get_environ_proxies:
  - args:
      no_proxy: null
      url: null
  requests.utils.get_netrc_auth:
  - args:
      raise_errors: null
      url: false
  requests.utils.get_unicode_from_response:
  - args:
      r: null
  requests.utils.guess_filename:
  - args:
      obj: null
  requests.utils.guess_json_utf:
  - args:
      data: null
  requests.utils.is_ipv4_address:
  - args:
      string_ip: null
  requests.utils.is_valid_cidr:
  - args:
      string_network: null
  requests.utils.iter_slices:
  - args:
      slice_length: null
      string: null
  requests.utils.parse_dict_header:
  - args:
      value: null
  requests.utils.parse_header_links:
  - args:
      value: null
  requests.utils.parse_list_header:
  - args:
      value: null
  requests.utils.prepend_scheme_if_needed:
  - args:
      new_scheme: null
      url: null
  requests.utils.requote_uri:
  - args:
      uri: null
  requests.utils.rewind_body:
  - args:
      prepared_request: null
  requests.utils.select_proxy:
  - args:
      proxies: null
      url: null
  requests.utils.should_bypass_proxies:
  - args:
      no_proxy: null
      url: null
  requests.utils.stream_decode_response_unicode:
  - args:
      iterator: null
      r: null
  requests.utils.super_len:
  - args:
      o: null
  requests.utils.to_key_val_list:
  - args:
      value: null
  requests.utils.to_native_string:
  - args:
      encoding: null
      string: ascii
  requests.utils.unquote_header_value:
  - args:
      is_filename: null
      value: false
  requests.utils.unquote_unreserved:
  - args:
      uri: null
  requests.utils.urldefragauth:
  - args:
      url: null
```

to a much shorter and simpler:

```yaml
requests:
  filename: /home/vanessa/anaconda3/lib/python3.7/site-packages/requests/__init__.py
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
for the result. Also notice the `istrue` statement isn't targeting a `{% raw %}{{ result }}{% endraw %}`
template that can be converted to a string and evaluated, but rather the GridTest
instance directly (self.result) and more specifically, the status_code attribute.

You might next want to browse other [tutorials]({{ site.baseurl }}/tutorials/) available.
