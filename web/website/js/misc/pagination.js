export function get_pager(data)
{
    return {
        get_full_path() { return data.current_path || location.href },
        has_previous() { return data.previous !== null },
        has_next() { return data.next !== null },
        previous_page_number() {
            return data.current_page_number > 1
                    ? data.current_page_number - 1
                    : null
        },
        next_page_number() {
            return data.current_page_number < data.total_pages
                    ? data.current_page_number + 1
                    : null
        },
        start_index() {
            return (data.current_page_number - 1) * data.page_size + 1
        },
        end_index() {
            let end = data.current_page_number * data.page_size;
            return end > data.total_objects ? data.total_objects : end;
        },

        pagination: {
            num_pages: data.total_pages,
            per_page: data.page_size,
            count: data.total_objects,
        },
    }
}
