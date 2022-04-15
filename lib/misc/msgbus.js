import { findIndex } from 'lodash';
//-
import { MessageBus } from './jsfw/core/msgbus.js';

let csrf_token = read_csrf_token();


function read_csrf_token()
{
    // store csrftoken
    let cookies = document.cookie.split(';').map(x => x.trim());
    let c_index = findIndex(cookies, o => o.indexOf('csrftoken') === 0);
    if (c_index !== -1)
    {
        return cookies[c_index].split('=')[1];
    }
}


function msgbus_options_callback(options)
{
    options.headers = options.headers || {};
    options.headers['X-CSRFToken'] = csrf_token;
}


export function msgbus(url, options)
{
    return new MessageBus(url, options, msgbus_options_callback);
}
