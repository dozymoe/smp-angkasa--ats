import { attach_modal } from '../../misc/modal';
import { msgbus } from '../../../../misc/msgbus';


export function InjectReSTPreview(element, app)
{
    const modal_id = 'modal-rest-preview';

    let modal = document.getElementById(modal_id);
    if (!modal) return;

    element.addEventListener('click', function()
    {
        let [modal, component] = attach_modal(modal_id);
        component.show();

        let textarea = document.getElementById(
                element.getAttribute('data-provide-rest-preview'));

        let formData = new FormData();
        formData.append('body', textarea.value);
        msgbus('/api/render-html').body(formData).post()
                .then(function(resp)
                {
                    return resp.text();
                })
                .then(function(html)
                {
                    modal.querySelector('.bx--modal-content').innerHTML = html;
                });
    });
}
