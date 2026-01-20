export interface CityI {
  id: string
  name: string
  name_en: string
  city_type: string
  lat: number
  lon: number
  community: string
  district: string
  region: string
  country: string
  full_name: string
}

export interface CityMetaI {
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

export interface CitiesI {
  items: CityI[]
  meta: CityMetaI
}
