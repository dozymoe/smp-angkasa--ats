import m from 'mithril/hyperscript';
import m_mount from 'mithril/mount';
//--
import { FileSelectModal } from './file-select-modal';
import { RestPreviewModal } from './rest-preview-modal';


export class CreatePage
{
    constructor(app)
    {
        this.app = app;
    }

    view(vnode)
    {
    }

    oncreate(vnode)
    {
        let cPreview = new RestPreviewModal(this.app);
        let cFileSelect = new FileSelectModal(this.app);

        m_mount(document.getElementById('js_modal-1'),
                {
                    view()
                    {
                        return m.fragment(null,
                        [
                            m(cPreview),
                            m(cFileSelect),
                        ])
                    },
                });
    }
}
