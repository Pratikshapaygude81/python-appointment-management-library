class RBAC:
     """
    Manages role-based access control in the hospital system.

    Stores permissions assigned to different user roles.
    """
     def __init__ (self):
          self.role_permissions ={
               "patient":[
                    "book_appointment",
                    "view_appointments"
               ],
               "doctor":[
                    "view_appointments"
               ],
               "admin":[
                    "manage_users",
                    "manage_appointments"
               ]
          }
     def check_permission(self,user_id:int,role:str,action:str)->bool:
          """
          check whether a role has permission to perform an action.
          Args:
              user_id(int):Id of the user
              role(str):users assigned role
              action(str):Action the user wants to perform

          Returns:
              bool:True if permission is granted otherwise False
          """
          if role not in self.role_permissions:
               return False
          return action in self.role_permissions[role]
          