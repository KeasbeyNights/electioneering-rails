class Politician
  include MongoMapper::Document

  key :name, String
  key :party, String
  key :type, String

  many :issues
end