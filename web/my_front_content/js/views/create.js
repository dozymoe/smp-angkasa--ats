import m from 'mithril/hyperscript';
import m_mount from 'mithril/mount';
//--
import { PageSelectModal } from './page-select-modal';


export class CreatePage
{
    constructor(app)
    {
        this.app = app;
    }

    view(node)
    {
    }

    oncreate(vnode)
    {
        let cPageSelect = new PageSelectModal(this.app);

        m_mount(document.getElementById('js_modal-1'), cPageSelect);
    }
}
