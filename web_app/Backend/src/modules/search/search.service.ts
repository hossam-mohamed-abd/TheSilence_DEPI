import { SearchRepository } from "./search.repository"; 

export class SearchService {
  private repository = new SearchRepository();

  async search(q: string, page: number, limit: number) {
    return this.repository.search(q, page, limit);
  }
}
