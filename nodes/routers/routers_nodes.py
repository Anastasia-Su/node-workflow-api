# from fastapi import APIRouter, HTTPException, status
# from dependencies import CommonDB
# from nodes import schemas, models
# from nodes.crud import crud_nodes
#
# router = APIRouter()
#
#
# @router.get("/nodes/", response_model=schemas.Node)
# def read_nodes(db: CommonDB):
#     return crud_nodes.get_node_list(db=db)
#
#
# @router.get("/nodes/{node_id}", response_model=schemas.Node)
# def read_single_node(node_id: int, db: CommonDB):
#     db_node = crud_nodes.get_node_detail(db=db, node_id=node_id)
#     if db_node is None:
#         raise HTTPException(status_code=404, detail="Node not found")
#     return db_node
#
#
# @router.post("/nodes/", response_model=schemas.Node)
# def create_node(node: schemas.NodeCreate, db: CommonDB):
#     if node.type not in [t for t in models.NodeTypes]:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Invalid node type. Must be one of: "
#             + ", ".join([t for t in models.NodeTypes]),
#         )
#     return crud_nodes.create_node(db=db, type=node.type)
#
#
# @router.put("/nodes/{node_id}", response_model=schemas.Node)
# def update_node(node_id: int, node: schemas.NodeCreate, db: CommonDB):
#     db_node = crud_nodes.update_node(
#         db=db, node_id=node_id, new_type=node.type
#     )
#     if db_node is None:
#         raise HTTPException(status_code=404, detail="Node not found")
#     return db_node
#
#
# @router.delete("/nodes/{node_id}", response_model=schemas.Node)
# def delete_node(node_id: int, db: CommonDB):
#     db_node = crud_nodes.delete_node(db=db, node_id=node_id)
#     if db_node is None:
#         raise HTTPException(status_code=404, detail="Node not found")
#     return db_node
#
#
# @router.get("/associations/", response_model=list[schemas.Node])
# def read_associations(db: CommonDB):
#     return crud_nodes.get_associations_list(db=db)
#
#
# @router.get("/associations/{node_id}", response_model=list[schemas.Node])
# def read_associations_for_node(node_id: int, db: CommonDB):
#     db_associations = crud_nodes.get_associations_for_node(
#         db=db, node_id=node_id
#     )
#     if db_associations is None:
#         raise HTTPException(status_code=404, detail="Node not found")
#     return db_associations
#
#
# @router.post("/associations/", response_model=schemas.Association)
# def create_association(association: schemas.AssociationCreate, db: CommonDB):
#     return crud_nodes.create_association(
#         db=db,
#         source_node_id=association.source_node_id,
#         target_node_id=association.target_node_id,
#     )
#
#
# @router.delete("/associations/", response_model=schemas.Association)
# def delete_association(association: schemas.Association, db: CommonDB):
#     db_association = crud_nodes.delete_association(
#         db=db,
#         source_node_id=association.source_node_id,
#         target_node_id=association.target_node_id,
#     )
#     if db_association is None:
#         raise HTTPException(status_code=404, detail="Association not found")
#     return db_association
