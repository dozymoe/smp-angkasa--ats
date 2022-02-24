import { showModal } from '../../../../../lib/fireh_react/core/views.jsx';
//-
import { SelectFile } from './views/modals.jsx';


export function InjectSelectFile(element, app)
{
    element.addEventListener('click', function()
    {
        let title = element.getAttribute('title') || "Select File";
        let elValue = document.getElementById(element.getAttribute(
                'data-provide-select_file'));
        let elLabel = document.getElementById(element.getAttribute(
                'data-select_file-label'));

        showModal(SelectFile, {title: title, selected: elValue.value}, app)
                .then(function(values)
                {
                    elValue.value = values.id;
                    elLabel.value = values.description;
                });
    });
}
