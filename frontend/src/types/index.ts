// API Response types
export interface Stop {
  id: number;
  name: string;
  latitude: number;
  longitude: number;
}

export interface Route {
  id: number;
  name: string;
  code: string;
  color?: string;
  description?: string;
  type?: string;
}

export interface RouteStop {
  id: number;
  route_id: number;
  stop_id: number;
  stop_order: number;
}

export interface StopInRoute extends Stop {
  stop_order: number;
}
