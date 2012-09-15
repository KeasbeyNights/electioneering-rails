ElectioneeringRails::Application.routes.draw do
  match "compare" => "home#compare"

  root :to => 'home#index'
end
