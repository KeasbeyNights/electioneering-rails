class Issue
  include MongoMapper::Document

  key :name, String
  key :stance, String
  
  belongs_to :politician
end