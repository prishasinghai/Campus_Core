// Base44 Mock Client Configuration
export const base44 = {
  entities: {
    Item: {
      list: async (sort, limit) => [],
      update: async (id, data) => ({ id, ...data })
    },
    Announcement: {
      list: async (sort, limit) => []
    }
  }
};
