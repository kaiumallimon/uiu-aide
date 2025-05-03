class SupabaseUser:
    def __init__(self, profile_data):
        self.profile_data = profile_data
        self.is_authenticated = True 
    
    def __getitem__(self, key):
        return self.profile_data[key]
    
    def get(self, key, default=None):
        return self.profile_data.get(key, default)
    
    def __contains__(self, key):
        return key in self.profile_data
