import React from 'react';
import ReactDOM from 'react-dom';


export function InjectWysiwyg(app, element)
{
    if (element.readOnly || element.disabled)
    {
        return;
    }

    let wrapper = element.closest('span');
    let el = document.createElement('div');
    element.style.display = 'none';
    wrapper.appendChild(el);
    ReactDOM.render(
            <div/>,
            el);
}
