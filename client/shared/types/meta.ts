export interface MetaI {
  page: number
  per_page: number
  total_items: number
  total_pages: number
  prev_page: number
  next_page: number
  links: {
    current: string
    next: string
    prev: string
  }
}
