import React from 'react';
import ReactDOM from 'react-dom';
//-
import { showModal } from '../../../../../lib/fireh_react/core/views.jsx';
import { ReSTPreview } from './views/modals.jsx';


export function InjectReSTPreview(app, element)
{
    let textarea = document.getElementById(
            element.getAttribute('data-provide-rest-preview'));

    element.addEventListener('click', function()
    {
        let title = element.getAttribute('title') || "Preview";
        let markup = textarea.value;

        showModal(ReSTPreview, {title: title, markup: markup}, app);
    });
}
