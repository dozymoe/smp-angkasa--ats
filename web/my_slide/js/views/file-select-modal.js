import CarbonModal from 'carbon-components/src/components/modal/modal';
import m from 'mithril/hyperscript';
import m_redraw from 'mithril/redraw';
import createStore from 'unistore';
import { mapActions } from 'unistore/src/util';
//--
import { msgbus } from '../../../misc/msgbus';
import { Slot } from '../../../misc/carbondesign-js/base';
import { Modal } from '../../../misc/carbondesign-js/modal';
import { Table, Th, Td, TdOvButton
       } from '../../../misc/carbondesign-js/data-table';
import { get_pager } from '../../../website/js/misc/pagination';

const ATTRIBUTE_NAME = 'data-provide-select_file';


const StoreActions =
{
    setObjects(state, objects)
    {
        return {objects: objects}
    },

    setPager(state, pager)
    {
        return {pager: pager}
    }
}


export class FileSelectModal
{
    constructor(app)
    {
        this.app = app;
        this.txt_title = gettext("File Select");
    }

    oninit(vnode)
    {
        this.store = createStore({
            pager: get_pager({}),
            objects: [],
        });
        this.actions = mapActions(StoreActions, this.store);

        this.ontrigger_click = this.ontrigger_click.bind(this);
    }

    view(vnode)
    {
        let state = this.store.getState();

        return (
//##
m(Modal, null, [
  m(Slot,
    {name: 'heading'},
    this.txt_title),
  m(Table,
    {
      pager: state.pager,
      pager_size: state.pager.pagination.per_page,
    },
    [
      m(Slot, {name: 'title'}, gettext("Slides")),
      m(Slot,
        {
          name: 'head',
        },
        [
          m(Th, null, gettext("Id")),
          m(Th, null, gettext("Image")),
          m(Th, null, gettext("Description")),
          m(Th, {mode: 'menu'}),
        ]),

      ...state.objects.map(obj =>
        m('tr', null,
          [
            m(Td, null, obj.id),
            m(Td, null,
              m('img',
                {
                  height: 100,
                  src: obj.attr_src,
                  srcset: obj.attr_srcset,
                  sizes: obj.attr_sizes,
                  style: {margin: 4},
                  alt: obj.alt_text,
                })),
            m(Td, null, obj.description),
            m(Td, {mode: 'menu'},
              [
                m(TdOvButton,
                  {
                    onclick: () => this.onselect_click(obj),
                  },
                  gettext("Select")),
              ]),
          ])
        ),
    ]),
  ])
//##
        )
    }

    oncreate(vnode)
    {
        this.component = CarbonModal.create(vnode.dom);

        for (let btn of document.querySelectorAll('button[' + ATTRIBUTE_NAME +
                ']'))
        {
            btn.addEventListener('click', this.ontrigger_click);
        }
    }

    onremove(vnode)
    {
        for (let btn of document.querySelectorAll('button[' + ATTRIBUTE_NAME +
                ']'))
        {
            btn.removeEventListener('click', this.ontrigger_click);
        }

        this.component.release();
    }

    onselect_click(obj)
    {
        let elValue = document.getElementById(this.button.getAttribute(
                'data-provide-select_file'));
        let elLabel = document.getElementById(this.button.getAttribute(
                'data-select_file-label'));
        elValue.value = obj.id;
        elLabel.value = obj.description;
        this.component.hide();
    }

    async ontrigger_click(event)
    {
        this.button = event.target || event.currentTarget;
        let textarea = document.getElementById(this.button.getAttribute(
                ATTRIBUTE_NAME));

        this.component.show();

        let resp = await msgbus('/api/files/').get();
        let body = await resp.json();
        this.actions.setPager(get_pager(body));
        this.actions.setObjects(body.results);
        m_redraw();
    }
}
