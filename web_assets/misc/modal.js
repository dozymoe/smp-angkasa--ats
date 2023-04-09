import Modal from 'carbon-components/src/components/modal/modal';

export function attach_modal(element_id)
{
    let element = document.getElementById(element_id);
    if (!element)
    {
        return [null, null];
    }

    let component = Modal.create(element);
    element.addEventListener('modal-hidden', () =>
            {
                component.release();
            },
            {
                once: true,
            });

    return [element, component]
}
