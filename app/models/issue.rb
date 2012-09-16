class Issue
  include MongoMapper::Document

  key :name, String
  key :stance, String
  
  belongs_to :politician

  def colorize(that)
    if self.name.eql?('Abortion') || self.name.eql?('Education') || 
      self.name.eql?('Energy and the Environment') || 
      self.name.eql?('Gay Marriage') || self.name.eql?('Health Care') ||
      self.name.eql?('Immigration')
      if self.stance.eql?(that.stance)
        "green"
      else
        "red"
      end
    else
      "blue"
    end
  end
end