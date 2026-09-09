"""
Database helper functions for interacting with Supabase
"""
from supabase import Client
from typing import Dict, List, Optional, Any

class DatabaseHelper:
    """Helper class for database operations"""
    
    def __init__(self, supabase_client: Client):
        self.client = supabase_client
    
    # User operations
    def authenticate_user(self, tic_email: str, password: str) -> Optional[Dict]:
        """Authenticate user by email and password"""
        try:
            response = self.client.table('Users').select('*').eq('tic_mail', tic_email).execute()
            if response.data and len(response.data) > 0:
                user = response.data[0]
                # In production, use bcrypt for password comparison
                if user['password'] == password:
                    return user
            return None
        except Exception as e:
            print(f"Authentication error: {str(e)}")
            return None
    
    def get_user_by_email(self, email: str) -> Optional[Dict]:
        """Get user by email"""
        try:
            response = self.client.table('Users').select('*').eq('tic_mail', email).execute()
            if response.data and len(response.data) > 0:
                return response.data[0]
            return None
        except Exception as e:
            print(f"Error fetching user: {str(e)}")
            return None
    
    # College operations
    def get_college_by_tic_email(self, tic_email: str) -> Optional[Dict]:
        """Get college details by TIC email"""
        try:
            response = self.client.table('College_Details').select('*').eq('Tic_Email', tic_email).execute()
            if response.data and len(response.data) > 0:
                return response.data[0]
            return None
        except Exception as e:
            print(f"Error fetching college: {str(e)}")
            return None
    
    def get_college_by_id(self, college_id: int) -> Optional[Dict]:
        """Get college details by college ID"""
        try:
            response = self.client.table('College_Details').select('*').eq('College_Code', college_id).execute()
            if response.data and len(response.data) > 0:
                return response.data[0]
            return None
        except Exception as e:
            print(f"Error fetching college: {str(e)}")
            return None
    
    # Course Teaching Details operations
    def add_teaching_detail(self, teaching_data: Dict) -> Optional[Dict]:
        """Add new course teaching detail"""
        try:
            response = self.client.table('College_Course_Teaching_Details').insert(teaching_data).execute()
            if response.data and len(response.data) > 0:
                return response.data[0]
            return None
        except Exception as e:
            print(f"Error adding teaching detail: {str(e)}")
            return None
    
    def get_teaching_details_by_college(self, college_id: int) -> List[Dict]:
        """Get all teaching details for a college"""
        try:
            response = self.client.table('College_Course_Teaching_Details').select('*').eq('College_id', college_id).execute()
            return response.data if response.data else []
        except Exception as e:
            print(f"Error fetching teaching details: {str(e)}")
            return []
    
    def get_teaching_detail_by_id(self, detail_id: int) -> Optional[Dict]:
        """Get teaching detail by ID"""
        try:
            response = self.client.table('College_Course_Teaching_Details').select('*').eq('id', detail_id).execute()
            if response.data and len(response.data) > 0:
                return response.data[0]
            return None
        except Exception as e:
            print(f"Error fetching teaching detail: {str(e)}")
            return None
    
    def update_teaching_detail(self, detail_id: int, update_data: Dict) -> bool:
        """Update teaching detail"""
        try:
            self.client.table('College_Course_Teaching_Details').update(update_data).eq('id', detail_id).execute()
            return True
        except Exception as e:
            print(f"Error updating teaching detail: {str(e)}")
            return False
    
    def delete_teaching_detail(self, detail_id: int) -> bool:
        """Delete teaching detail"""
        try:
            self.client.table('College_Course_Teaching_Details').delete().eq('id', detail_id).execute()
            return True
        except Exception as e:
            print(f"Error deleting teaching detail: {str(e)}")
            return False
    
    # Paper operations
    def get_paper_by_code(self, upc_code: int) -> Optional[Dict]:
        """Get paper details by UPC code"""
        try:
            response = self.client.table('Paper_Details').select('*').eq('UPC_Code', upc_code).execute()
            if response.data and len(response.data) > 0:
                return response.data[0]
            return None
        except Exception as e:
            print(f"Error fetching paper: {str(e)}")
            return None
    
    def get_papers_by_semester(self, semester: int) -> List[Dict]:
        """Get all papers for a semester"""
        try:
            response = self.client.table('Paper_Details').select('*').eq('Semester', semester).execute()
            return response.data if response.data else []
        except Exception as e:
            print(f"Error fetching papers: {str(e)}")
            return []
    
    # Program operations
    def get_all_programs(self) -> List[Dict]:
        """Get all course programs from College_Course_Program_Details"""
        try:
            response = self.client.table('College_Course_Program_Details').select('*').execute()
            return response.data if response.data else []
        except Exception as e:
            print(f"Error fetching programs: {str(e)}")
            return []
    
    # Utility operations
    def search_teaching_details(self, college_id: int, search_term: str) -> List[Dict]:
        """Search teaching details by teacher name or paper name"""
        try:
            response = self.client.table('College_Course_Teaching_Details').select('*').eq('College_id', college_id).execute()
            if response.data:
                search_term = search_term.lower()
                filtered = [
                    item for item in response.data
                    if search_term in item.get('Teacher_Name', '').lower()
                    or search_term in item.get('paper_name', '').lower()
                ]
                return filtered
            return []
        except Exception as e:
            print(f"Error searching teaching details: {str(e)}")
            return []
