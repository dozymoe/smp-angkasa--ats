import m_mount from 'mithril/mount';
//--
import { ApplicationStorage } from './fw/core/application';

export class Application extends ApplicationStorage
{
    modal_index = 0;

    startModal(component)
    {
        this.modal_index += 1;
        m_mount(document.getElementById(`js_modal-${this.modal_index}`),
                component);
    }

    stopModal()
    {
        m_mount(document.getElementById(`js_modal-${this.modal_index}`), null);
        this.modal_index -= 1;
    }
}
