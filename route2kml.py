# ------------------------------------------------------------------
# Author: Fang (Alicia) Tang
# Email: fangt@asu.edu
# Date: 03/04/2025
# ------------------------------------------------------------------


import os
import pandas as pd
import simplekml


def main():
    # Create output folder if it doesn't exist
    output_folder = "outputs"
    os.makedirs(output_folder, exist_ok=True)

    # ------------------------------------------------------------------
    # 1) Read node.csv (node_id, zone_id, x_coord, y_coord)
    # ------------------------------------------------------------------
    nodes_df = pd.read_csv("node.csv")

    # Create a dictionary to map node_id -> (longitude, latitude)
    # (Assuming x_coord is longitude and y_coord is latitude)
    node_coords = {}
    for idx, row in nodes_df.iterrows():
        node_id = row["node_id"]
        lon = row["x_coord"]
        lat = row["y_coord"]
        node_coords[node_id] = (lon, lat)

    # ------------------------------------------------------------------
    # 2) Read route_assignment.csv
    # (mode, route_id, o_zone_id, d_zone_id, unique_route_id, prob,
    #  node_ids, link_ids, distance_mile, total_distance_km,
    #  total_free_flow_travel_time, total_travel_time, route_key, volume)
    # ------------------------------------------------------------------
    routes_df = pd.read_csv("route_assignment.csv")

    # ------------------------------------------------------------------
    # 3) Generate KML for each route
    # ------------------------------------------------------------------
    for idx, route_row in routes_df.iterrows():
        # Parse the node_ids string ("1;547;549;...") into a list of ints
        node_list_str = route_row["node_ids"]
        node_id_strs = node_list_str.split(";")

        # Convert each node_id string to an integer and look up coordinates
        route_coords = []
        for nid_str in node_id_strs:
            nid = int(nid_str)
            if nid in node_coords:
                route_coords.append(node_coords[nid])
            else:
                print(f"Warning: node {nid} not found in node_coords.")

        # Create a KML object
        kml = simplekml.Kml()

        # Create a LineString for this route
        linestring = kml.newlinestring(name=f"Route_{idx}")
        # Assign the coordinates to the LineString
        linestring.coords = route_coords

        # Optional: Add description or style
        linestring.description = (
            f"Mode: {route_row['mode']} | "
            f"o_zone_id: {route_row['o_zone_id']} | "
            f"d_zone_id: {route_row['d_zone_id']} | "
            f"Volume: {route_row['volume']}"
        )
        # For example, make the line red and thicker:
        linestring.style.linestyle.color = simplekml.Color.red
        linestring.style.linestyle.width = 3

        # Save each route to a separate KML file in the output folder
        kml_filename = os.path.join(output_folder, f"route_{idx}.kml")
        kml.save(kml_filename)
        print(f"Saved {kml_filename}")


if __name__ == "__main__":
    main()