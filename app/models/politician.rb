class Politician
  include MongoMapper::Document

  key :name, String
  key :party, String
  key :candidate_type, String

  many :issues
end