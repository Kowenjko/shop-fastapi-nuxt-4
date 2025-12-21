export const useBaseUrlApi = () => {
  const { apiBaseUrl, apiBaseUrlServer } = useRuntimeConfig().public

  const baseURL = process.server ? (apiBaseUrlServer as string) : (apiBaseUrl as string)
  return { baseURL, apiBaseUrlServer, apiBaseUrl }
}
