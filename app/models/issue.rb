class Issue
  include MongoMapper::Document

  key :name, String
  key :stance, String
  
  belongs_to :politician

  def colorize(that)
    if (self.politician.name.eql?('Mitt Romney') && 
      that.politician.name.eql?('Paul Ryan')) ||
      (self.politician.name.eql?('Paul Ryan') && 
      that.politician.name.eql?('Mitt Romney'))
      if self.name.eql?('Entitlements')
        return 'green'
      elsif self.name.eql?('Foreign Policy')
        return 'green'
      elsif self.name.eql?('Gun Policy')
        return 'yellow'
      elsif self.name.eql?('Jobs')
        return 'green'
      elsif self.name.eql?('Taxes')
        return 'yellow'
      end

    elsif (self.politician.name.eql?('Mitt Romney') && 
      that.politician.name.eql?('Barack Obama')) ||
      (self.politician.name.eql?('Barack Obama') && 
      that.politician.name.eql?('Mitt Romney'))
      if self.name.eql?('Entitlements')
        return 'red'
      elsif self.name.eql?('Foreign Policy')
        return 'red'
      elsif self.name.eql?('Gun Policy')
        return 'yellow'
      elsif self.name.eql?('Jobs')
        return 'red'
      elsif self.name.eql?('Taxes')
        return 'red'
      end

    elsif (self.politician.name.eql?('Paul Ryan') && 
      that.politician.name.eql?('Barack Obama')) ||
      (self.politician.name.eql?('Barack Obama') && 
      that.politician.name.eql?('Paul Ryan'))
      if self.name.eql?('Entitlements')
        return 'red'
      elsif self.name.eql?('Foreign Policy')
        return 'red'
      elsif self.name.eql?('Gun Policy')
        return 'yellow'
      elsif self.name.eql?('Jobs')
        return 'red'
      elsif self.name.eql?('Taxes')
        return 'red'
      end

    elsif (self.politician.name.eql?('Joe Biden') && 
      that.politician.name.eql?('Barack Obama')) ||
      (self.politician.name.eql?('Barack Obama') && 
      that.politician.name.eql?('Joe Biden'))
      if self.name.eql?('Entitlements')
        return 'green'
      elsif self.name.eql?('Foreign Policy')
        return 'green'
      elsif self.name.eql?('Gun Policy')
        return 'green'
      elsif self.name.eql?('Jobs')
        return 'green'
      elsif self.name.eql?('Taxes')
        return 'green'
      end

    elsif (self.politician.name.eql?('Joe Biden') && 
      that.politician.name.eql?('Paul Ryan')) ||
      (self.politician.name.eql?('Paul Ryan') && 
      that.politician.name.eql?('Joe Biden'))
      if self.name.eql?('Entitlements')
        return 'red'
      elsif self.name.eql?('Foreign Policy')
        return 'yellow'
      elsif self.name.eql?('Gun Policy')
        return 'red'
      elsif self.name.eql?('Jobs')
        return 'red'
      elsif self.name.eql?('Taxes')
        return 'red'
      end

    elsif (self.politician.name.eql?('Joe Biden') && 
      that.politician.name.eql?('Mitt Romney')) ||
      (self.politician.name.eql?('Mitt Romney') && 
      that.politician.name.eql?('Joe Biden'))
      if self.name.eql?('Entitlements')
        return 'red'
      elsif self.name.eql?('Foreign Policy')
        return 'yellow'
      elsif self.name.eql?('Gun Policy')
        return 'yellow'
      elsif self.name.eql?('Jobs')
        return 'red'
      elsif self.name.eql?('Taxes')
        return 'red'
      end

    elsif (self.politician.name.eql?('Barack Obama') && 
      that.politician.name.eql?('Gary Johnson')) ||
      (self.politician.name.eql?('Gary Johnson') && 
      that.politician.name.eql?('Barack Obama'))
      if self.name.eql?('Entitlements')
        return 'red'
      elsif self.name.eql?('Foreign Policy')
        return 'red'
      elsif self.name.eql?('Gun Policy')
        return 'red'
      elsif self.name.eql?('Jobs')
        return 'red'
      elsif self.name.eql?('Taxes')
        return 'red'
      end

    elsif (self.politician.name.eql?('Mitt Romney') && 
      that.politician.name.eql?('Gary Johnson')) ||
      (self.politician.name.eql?('Gary Johnson') && 
      that.politician.name.eql?('Mitt Romney'))
      if self.name.eql?('Entitlements')
        return 'green'
      elsif self.name.eql?('Foreign Policy')
        return 'red'
      elsif self.name.eql?('Gun Policy')
        return 'yellow'
      elsif self.name.eql?('Jobs')
        return 'green'
      elsif self.name.eql?('Taxes')
        return 'yellow'
      end

    end

    if self.name.eql?('Abortion') || self.name.eql?('Education') || 
      self.name.eql?('Energy') || 
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